# Assay Report — No. 002

**Subject:** M6 Financial Forecasting & Investment Competition — public organizer data<br>
**Assay ID:** RL-A-002 · **Analysis run:** 2026-08-16 · **Published:** 2026-09-29 · **Report version:** 1.2 · **Report format:** Assay Schema v0.1<br>
**Analyst:** Chris Deschenes · **Independence:** No financial interest in any participating team. Before the claim was registered, contact with the dataset was structural only — no scores, ranks, or outcomes (§7.1).

## §0 — Verdict

**0.1 Overall verdict: Supported with conditions.**

**0.2 Basis.** Rank on the forecasting track (RPS) persists from the first six months of M6 into the second six months, far beyond what luck produces across the population, and the first-half top decile lands well above a random draw in the second half. Rank on the investment track (IR) does not persist distinguishably from luck. The test that produced these results — a split-half persistence design — was chosen after the claim was registered and before any scores were examined; the registration file does not describe it. Under the registration's own rule and schema §7.5, that deviation caps the overall verdict at Supported with conditions.

**0.3 Headline estimates.** Split-half rank persistence, M1–M6 vs M7–M12, 197 teams with ≥3 scored months in each half. Spearman ρ; one-sided permutation p (20,000 shuffles, seed 20260816; the smallest attainable p is 1/20,001, reported as < 0.0001); team-level bootstrap 95% interval (10,000 resamples, same seed; added in v1.2, descriptive).

| Track | ρ | 95% interval | Permutation p | Top-decile check |
|---|---|---|---|---|
| **RPS** (forecasting) — registered | 0.695 | [0.58, 0.79] | < 0.0001 | mean half-B rank 56.4 vs 99.1 null (≈3.4σ), p = 0.0002 |
| **IR** (investment) — registered | 0.055 | [−0.10, 0.21] | 0.22 | not run; bulk result null |
| **OR** (duathlon) — *post-registration* | 0.644 | [0.54, 0.73] | < 0.0001 | mean half-B rank 36.9 vs 99.1 null (≈5.0σ), p < 0.0001 |

**0.4 Claims table.**

*Registered claims (frozen 2026-08-16; the registration names RPS and IR as the organizers' track metrics):*

| Claim | Verdict | Decided in |
|---|---|---|
| Top-ranked RPS (forecasting) performance is distinguishable from luck | **Supported with conditions** — test operationalized after registration (§7.2); holds for the 197 teams with data in both halves, at a six-month horizon | §5, §7 |
| Top-ranked IR (investment) performance is distinguishable from luck | **Not supported** — cannot be distinguished from luck at this horizon; the interval does not rule out modest persistence | §4, §7 |

*Post-registration claim (added after the freeze; caveat permanent, per schema §1.2):*

| Claim | Verdict | Decided in |
|---|---|---|
| Top-ranked OR (duathlon) performance is distinguishable from luck | **Supported** as a post-registration result — not graded against a registered protocol | §5 |

**0.5 Findings summary:** 3 Major (protocol operationalized after registration; population scope of the registered claim; a data-parsing defect caught in-session), 0 Critical, several Notes, including the unrecorded model identity (§1.4).

## §1 — Scope & claim registration

**1.1 Engagement scope.** Independent, self-directed analysis of the public M6 dataset (`Mcompetitions/M6-methods`). Not commissioned. Assay No. 002 is the practice's second published case study and its first on third-party results.

**Prior work.** The question of how forecasting skill relates to investment skill is the M6 organizers' question, not this report's. Their published results report a limited connection between the forecasts teams submitted and the investment decisions they made (Makridakis, Spiliotis, Hollyman, Petropoulos, Swanson & Gaba, "The M6 forecasting competition: Bridging the gap between forecasting and investment decisions," *International Journal of Forecasting* 41(4), 2025, 1315–1354). This Assay asks a narrower question: does a team's rank on each track in the first six months predict its rank in the next six, by more than luck would?

**1.2 Registered claim.** Frozen 2026-08-16, before any performance data was examined, in `CLAIM_REGISTRATION.md` (published unmodified; SHA-256 `4bedd1c2…d3c2c8` as published — no hash was taken at freeze time, §7.1):

> "Top-ranked M6 performance is distinguishable from luck after multiplicity correction across the full 251-team population."

The registration names RPS (forecasting) and IR (investment) as the metrics, specifies a comparison of the top-ranked team or top decile against an all-teams-equally-skilled null with family-wise or FDR correction, and defines the population as all 251 submitting teams. It does not specify the split-half design, the per-half data threshold, or the permutation parameters used here. See §7.2.

**1.3 Artifact inventory.**

| Artifact | Role | SHA-256 |
|---|---|---|
| `assets_m6.csv` | Daily prices, M6 universe | `48c67aa0976ae63de3a6d7a42228ef374d39221734a433c9391572d01e85b20a` |
| `IJF paper/submissions.csv` | Raw submissions, 251 team IDs | `2615d352d04b19b99c0bba91da9bb835403580b5253b539ca75f429ea0408001` |
| `IJF paper/summary_leaderboard.xlsx` | Organizer-computed monthly RPS/IR/OR per team | `8d35b66b476be7587e574a08bfa83f550778639b0c69ff1bc790ccfde15f9bf4` |

Source: `github.com/Mcompetitions/M6-methods` at commit `10c553f7a5ffbaf53971ca48ea982b2c0dd952ed` (committed 2024-10-02). Hashes re-verified against that commit on 2026-09-24 and again on 2026-09-29; on both dates that commit was also the repository's HEAD.

**1.4 Environment and automation disclosure.** The analysis ran in a single agentic coding session using a Claude model via claude.ai; the specific model and version were not recorded at run time. The internal v1.0 draft named a specific model; that name was not taken from any run record and has been withdrawn. This is a gap against the practice's own disclosure rule and is logged as a Note. It does not affect any reported number: every figure was reproduced independently from the pinned inputs (below).
- **Deterministic (every reported number):** Spearman correlations, permutation p-values, bootstrap intervals, population counts — plain Python (pandas, scipy, numpy), seeded, re-runnable.
- **Agent-assisted:** data intake, structure discovery, anomaly triage (the static-submitter check), and drafting, under the analyst's direction.
- **Human:** claim registration, the choice to report every track, verdict sign-off.

No reported number was produced by model judgment. The session's analysis code was consolidated into `reproduce_assay002.py` for v1.1. For v1.2 the script was run fresh against the pinned commit on 2026-09-24, in a separate Claude session (Claude Opus 5.5), and reproduced every original figure exactly.

## §2 — Data lineage & point-in-time integrity

Not applicable in the usual sense. The Assay uses the organizers' finalized monthly scores rather than reconstructing forecasts from prices. M6's design — blind monthly submissions scored against subsequently realized prices — supplies point-in-time discipline at the source; this Assay inherits it rather than re-verifying it (§9.1).

## §3 — Leakage battery

**3.1–3.3.** Not applicable: a persistence test on already-realized, organizer-computed outcomes, with no analyst feature engineering.

**3.4 Selection effects — population accounting.**

```
Team IDs in submissions.csv                                 251
  minus: flagged inactive by the organizers, never scored   -25
Teams scored by the organizers (the organizers' 226)        226
  minus: joined after the start, ineligible for Global rank -63
Teams on the official Global leaderboard                    163
```

The 251 includes 25 team IDs that the organizers' own file marks `IsActive = 0` on every row; none received a score. The remaining 226 is the population the organizers report as having entered M6, and 163 of those joined at the start and were eligible for the global prizes; most of the other 63 joined at a later quarter (Makridakis et al., 2025). The persistence tests use the 197 of the 226 with at least three scored months in each half.

The registered claim said "the full 251-team population." No test can include teams that were never scored, and the 197-team threshold was set after registration. Both are disclosed as scope conditions.

**3.5 Findings:** Major — the registered claim's population cannot be tested as worded; resolved by full accounting, not by redefinition.

## §4 — Attribution & decomposition

Factor stripping and cost realism do not apply to a persistence test. The analogous decomposition is by track:

```
"M6 performance" (as registered, unscoped)
  ├─ RPS  forecasting    ρ = 0.695  [0.58, 0.79]   persists
  ├─ IR   investment     ρ = 0.055  [−0.10, 0.21]  not distinguishable from luck
  └─ OR   duathlon       ρ = 0.644  [0.54, 0.73]   persists (post-registration)
```

This is consistent with the organizers' published finding that forecasts and investment decisions were weakly connected; this report adds a pre-registered test of which track's ranking carries over in time. It does not explain why. One mechanical possibility is left open: a single month's information ratio is a noisy statistic, so rank on IR may be dominated by realized-return noise at a monthly resolution even where some skill exists. The interval on IR does not exclude modest persistence.

## §5 — Concentration & fragility

**5.1 Composition check — static submitters.** 596 of 2,423 team-months (24.6%) sit at RPS ≈ 0.160, consistent with a uniform-probability default submission. If many teams submitted that by default, "persistence" could mean persistent disengagement. 122 of the 226 scored teams were flagged as likely static (within-team std < 0.01, mean in [0.155, 0.165]); 109 of those are among the 197 eligible teams. Removing them leaves 88 teams: **ρ = 0.648, p < 0.0001**, against 0.695 on all 197. The static submitters do not explain the result.

**5.2 Top-decile check.** The registered claim is about top-ranked teams, not the average team. The first-half top decile (19 teams) was compared with 20,000 random same-size groups on second-half rank:

- RPS: mean half-B rank 56.4 vs a null of 99.1 (std 12.4), ≈3.4σ, p = 0.0002.
- OR: 36.9 vs 99.1 (std 12.4), ≈5.0σ, p < 0.0001.

**5.3 Not run.** Leave-top-k removal and subperiod stability beyond the single split were not run.

**5.4 Findings:** None; both checks run left the result standing.

## §6 — Calibration & uncertainty

Not applicable: this tests rank persistence, not the calibration of any team's probabilities. Calibration of the submitted quintile probabilities is a natural follow-on (§9.1).

## §7 — Pre-registered holdout

**7.1 Registration record.** `CLAIM_REGISTRATION.md` was written to disk on 2026-08-16, before the analysis clone and before any performance data was examined. It was not cryptographically committed at the time; its precedence rests on the session record. An earlier session had examined the dataset's structure — file schema, row and team-ID counts, evaluation periods — and the organizers' published 226/163 figures, which is where the claim's 251 came from. No scores, ranks, or outcome values were examined before registration. The file is published unmodified.

**7.2 Protocol deviation.** The registration specifies a top-team or top-decile test against an equal-skill null, with family-wise or FDR correction. The analysis instead used a split-half design: rank persistence from M1–M6 to M7–M12, a ≥3-months-per-half eligibility threshold, and a permutation null. That design was chosen after registration and before any scores were examined. It was not written down. It is graded here as a deviation, not as pre-specified.

The split-half design answers the registered question in a stricter form than the registered method would have: it asks whether top rank in one period predicts rank in an unseen later period, rather than whether one full-year rank is surprising in-sample. That is an argument for the choice, not a substitute for having registered it. Under registration step 7 and schema §7.5, the overall verdict is capped at Supported with conditions.

**7.3 Population accounting.** §3.4. All exclusions are counted and disclosed.

**7.4 Multiplicity.** Two statistics carry the claims: the bulk permutation test on ρ, which tests population-level persistence against exchangeable ranks, and the top-decile test, which compares the actual top group with random same-size groups and so accounts for the top being selected from 197 teams. Three tracks were tested; RPS and OR clear any reasonable correction for three tests by orders of magnitude, and IR is null without one.

**7.5 Result.** Reported above. The split-half analysis was run once. OR was added after registration and is reported separately. Bootstrap intervals were added in v1.2 and change no p-value or verdict.

## §8 — Reproducibility & provenance

**8.1 Code and data.** The registration file, `reproduce_assay002.py`, the original session outputs, and the 2026-09-24 reproduction output are published at [github.com/Entrasoft/assay-002](https://github.com/Entrasoft/assay-002) (tag `v1.2`). The script verifies the three input hashes and fails on mismatch.

**8.2 Determinism.** Seed 20260816 throughout. Against the pinned commit, the script reproduces every figure in this report exactly.

**8.3 A defect caught in-session.** An early population count compared `RankGlobal` with the string `'NA'` and found zero unranked teams. It was silently wrong: pandas had already parsed `"NA"` into `NaN`, so the comparison could never match. The analyst caught it by inspecting the column's type and value counts, and fixed it with explicit coercion. The corrected figure — 63 scored but unranked, 88 of 251 absent from the leaderboard — is the one reported. A caught bug is disclosed so that readers can weigh the ones that weren't caught.

## §9 — Limitations, conditions & expiry

**9.1 Out of scope.** No point-in-time reconstruction of any team's process (§2). No calibration analysis (§6). No causal account of why forecasting rank persists and investment rank does not (§4).

**9.2 Validity conditions.** Holds for the M6 data at the §1.3 hashes. A revised leaderboard or different track weighting requires a re-run.

**9.3 Expiry.** None natural; the competition is closed. Re-run if the source repository changes.

**9.4 What would falsify this report.** A corrected version of the organizers' monthly scores that materially changes the split-half correlations, or an error in the permutation or bootstrap implementation found by re-running the published script against the pinned inputs.

## Revision history

**v1.2 (2026-09-29, publication).**

1. The registration file does not contain the split-half design, per-half threshold, or permutation parameters that v1.1 described as registered. The design is now reported as chosen after registration (§7.2), logged as a Major finding, and the registered claims are graded accordingly. The overall verdict is unchanged; it was already at the cap.
2. OR, not named in the registration, moved to a post-registration table.
3. v1.1 described OR as the metric that determined the prizes. M6 awarded prizes on the forecasting, investment, and duathlon tracks; OR is the duathlon ranking.
4. Population reconciled to the organizers' published figures; the 25 unscored IDs identified as organizer-flagged inactive (§3.4).
5. Organizers' prior work cited in §1.1 and §4.
6. p-values at the permutation floor reported as < 0.0001. Bootstrap intervals added (§0.3). "Strongly supported" removed.
7. §5.1 arithmetic corrected (88 = 197 eligible − 109 static), relabeled a composition check; checks not run are listed.
8. Hash re-verification dated (2026-09-24, 2026-09-29); the reproduction run disclosed (§1.4).
9. Model identity for the 2026-08-16 session disclosed as not recorded; the model named in v1.0 withdrawn (§1.4).

**v1.1.** Corrected three statements in the internal v1.0 draft: structural reconnaissance preceded registration; the registration was not hashed; analysis code was consolidated into a reproduction script. No numbers changed.
