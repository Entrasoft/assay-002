"""
Assay No. 002 — M6 persistence analysis: reproduction script.

Reproduces every number in the Assay No. 002 report from the public M6 data.

Inputs (pinned):
    git clone https://github.com/Mcompetitions/M6-methods.git
    git -C M6-methods checkout 10c553f7a5ffbaf53971ca48ea982b2c0dd952ed
    Expected SHA-256:
      IJF paper/summary_leaderboard.xlsx  8d35b66b476be7587e574a08bfa83f550778639b0c69ff1bc790ccfde15f9bf4
      IJF paper/submissions.csv           2615d352d04b19b99c0bba91da9bb835403580b5253b539ca75f429ea0408001
      assets_m6.csv                       48c67aa0976ae63de3a6d7a42228ef374d39221734a433c9391572d01e85b20a

Usage:
    python reproduce_assay002.py /path/to/M6-methods

All randomness is seeded (20260816). Each permutation test uses a fresh
generator with that seed, matching the original session's call order, so the
reported p-values reproduce exactly.
"""
import csv
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import openpyxl
import pandas as pd
from scipy.stats import spearmanr

SEED = 20260816
N_PERM = 20000
N_BOOT = 10000  # supplementary intervals, added in report v1.2 (post-analysis, descriptive only)
MIN_MONTHS_PER_HALF = 3
MONTHS = [f"M{i}" for i in range(1, 13)]
HALF_A, HALF_B = MONTHS[:6], MONTHS[6:]

EXPECTED_SHA = {
    "IJF paper/summary_leaderboard.xlsx": "8d35b66b476be7587e574a08bfa83f550778639b0c69ff1bc790ccfde15f9bf4",
    "IJF paper/submissions.csv": "2615d352d04b19b99c0bba91da9bb835403580b5253b539ca75f429ea0408001",
    "assets_m6.csv": "48c67aa0976ae63de3a6d7a42228ef374d39221734a433c9391572d01e85b20a",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_sheet(wb, name: str) -> pd.DataFrame:
    rows = list(wb[name].iter_rows(values_only=True))
    df = pd.DataFrame(rows[1:], columns=rows[0]).dropna(subset=["Team"]).copy()
    df["TeamID"] = df["Team"].astype(str).apply(lambda s: s.split()[0])
    # The organizer marks missing values with the literal string "NA".
    # Coerce explicitly rather than relying on a parser's NA sniffing —
    # implicit coercion is the defect disclosed in report §8.3.
    for c in MONTHS + ["Global", "RankGlobal"]:
        df[c] = pd.to_numeric(df[c].replace("NA", pd.NA), errors="coerce")
    return df.reset_index(drop=True)


def halves(df: pd.DataFrame) -> pd.DataFrame:
    a, b = df[HALF_A], df[HALF_B]
    out = pd.DataFrame({
        "TeamID": df["TeamID"],
        "mean_a": a.mean(axis=1), "mean_b": b.mean(axis=1),
        "n_a": a.notna().sum(axis=1), "n_b": b.notna().sum(axis=1),
    })
    return out[(out.n_a >= MIN_MONTHS_PER_HALF) & (out.n_b >= MIN_MONTHS_PER_HALF)].copy()


def perm_test(sub: pd.DataFrame, higher_is_better: bool = False):
    """One-sided split-half rank-persistence test. Fresh seeded RNG per call."""
    r = np.random.default_rng(SEED)
    a, b = sub["mean_a"].values, sub["mean_b"].values
    if higher_is_better:
        a, b = -a, -b
    ra = pd.Series(a).rank(method="average").values
    rb = pd.Series(b).rank(method="average").values
    obs = spearmanr(ra, rb)[0]
    idx = np.arange(len(rb))
    ge = 0
    for _ in range(N_PERM):
        if spearmanr(ra, rb[r.permutation(idx)])[0] >= obs:
            ge += 1
    return float(obs), (ge + 1) / (N_PERM + 1), len(sub)


def boot_ci(sub: pd.DataFrame):
    """Supplementary: team-level bootstrap 95% interval on split-half Spearman rho.
    Added in report v1.2 after the original analysis; descriptive, not part of the verdict rule."""
    r = np.random.default_rng(SEED)
    a, b = sub["mean_a"].values, sub["mean_b"].values
    n = len(a)
    reps = [spearmanr(a[i], b[i])[0] for i in (r.integers(0, n, n) for _ in range(N_BOOT))]
    lo, hi = np.percentile(reps, [2.5, 97.5])
    return [float(lo), float(hi)]


def top_decile(elig: pd.DataFrame):
    """Mean half-B rank of the half-A top decile vs. random same-size groups."""
    elig = elig.copy()
    k = max(1, int(len(elig) * 0.10))
    top_ids = set(elig.sort_values("mean_a").head(k)["TeamID"])
    elig["rank_b"] = elig["mean_b"].rank(method="average")
    obs = elig.loc[elig.TeamID.isin(top_ids), "rank_b"].mean()
    rb = elig["rank_b"].values
    rng = np.random.default_rng(SEED)
    idx = np.arange(len(elig))
    null = np.array([rb[rng.choice(idx, size=k, replace=False)].mean() for _ in range(N_PERM)])
    p = (np.sum(null <= obs) + 1) / (N_PERM + 1)
    return k, float(obs), float(null.mean()), float(null.std()), float(p)


def main(root: str) -> dict:
    root = Path(root)
    for rel, want in EXPECTED_SHA.items():
        got = sha256(root / rel)
        assert got == want, f"hash mismatch for {rel}: {got}"

    wb = openpyxl.load_workbook(root / "IJF paper/summary_leaderboard.xlsx",
                                data_only=True, read_only=True)
    rps, ir, orr = load_sheet(wb, "RPS"), load_sheet(wb, "IR"), load_sheet(wb, "OR")

    # §3.4 population accounting
    with open(root / "IJF paper/submissions.csv") as f:
        submitters = {row["Team"] for row in csv.DictReader(f)}
    with open(root / "IJF paper/submissions.csv") as f:
        inactive = {row["Team"] for row in csv.DictReader(f) if row["IsActive"] == "0"}
    scored = set(rps["TeamID"])
    ranked = set(rps.loc[rps["RankGlobal"].notna(), "TeamID"])
    population = {
        "submitted": len(submitters), "scored": len(scored), "ranked": len(ranked),
        "excluded_from_ranking": len(submitters - ranked),
        "never_scored": len(submitters - scored), "scored_not_ranked": len(scored - ranked),
        "never_scored_equals_organizer_inactive_flag": (submitters - scored) == inactive,
    }

    # §4 / §7 primary split-half tests
    rho_rps, p_rps, n_rps = perm_test(halves(rps))
    rho_ir, p_ir, n_ir = perm_test(halves(ir), higher_is_better=True)

    # §5.1 naive/static-submitter cluster
    vals = rps[MONTHS].values.flatten()
    vals = vals[~pd.isna(vals)].astype(float)
    cluster = int((np.round(vals, 3) == 0.160).sum())
    naive = (rps[MONTHS].std(axis=1) < 0.01) & rps[MONTHS].mean(axis=1).between(0.155, 0.165)
    elig_rps = halves(rps).merge(pd.DataFrame({"TeamID": rps["TeamID"], "naive": naive}), on="TeamID")
    rho_active, p_active, n_active = perm_test(elig_rps[~elig_rps.naive])

    # §5.2 top-decile checks
    k_r, obs_r, nm_r, ns_r, p_top_rps = top_decile(elig_rps)
    elig_or = halves(orr)
    rho_or, p_or, n_or = perm_test(elig_or)
    k_o, obs_o, nm_o, ns_o, p_top_or = top_decile(elig_or)

    ci = {"rps": boot_ci(halves(rps)), "ir": boot_ci(halves(ir)), "or": boot_ci(elig_or)}

    return {
        "population": population,
        "supplementary_bootstrap_ci95_rho": ci,
        "p_value_floor": 1 / (N_PERM + 1),
        "rps": {"n": n_rps, "rho": rho_rps, "p_perm": p_rps},
        "ir": {"n": n_ir, "rho": rho_ir, "p_perm": p_ir},
        "or": {"n": n_or, "rho": rho_or, "p_perm": p_or,
               "top_decile": {"k": k_o, "mean_rank_b": obs_o, "null_mean": nm_o,
                              "null_std": ns_o, "p": p_top_or}},
        "rps_robustness": {
            "cluster_0160_team_months": cluster, "total_team_months": int(len(vals)),
            "naive_flagged_teams": int(naive.sum()),
            "excl_naive": {"n": n_active, "rho": rho_active, "p_perm": p_active},
            "top_decile": {"k": k_r, "mean_rank_b": obs_r, "null_mean": nm_r,
                           "null_std": ns_r, "p": p_top_rps},
        },
        "config": {"seed": SEED, "n_perm": N_PERM, "n_boot": N_BOOT, "min_months_per_half": MIN_MONTHS_PER_HALF},
    }


if __name__ == "__main__":
    print(json.dumps(main(sys.argv[1] if len(sys.argv) > 1 else "M6-methods"), indent=2))
