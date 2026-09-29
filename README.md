# Assay No. 002 — M6 rank persistence

Relight Labs · published 2026-09-29 · essay: [Did the M6 Leaders Get Lucky?](https://essays.relightlabs.ai/did-the-m6-leaders-get-lucky/)

Does a team's rank in the first six months of the M6 forecasting competition predict its rank in the next six, by more than luck would?

| Track | ρ (M1–M6 → M7–M12, n = 197) | Verdict |
|---|---|---|
| RPS (forecasting) | 0.695 | Supported with conditions |
| IR (investment) | 0.055 | Not supported |
| OR (duathlon) | 0.644 | Supported (post-registration) |

Full report: [`Assay-002-M6-Report_v1.2.md`](Assay-002-M6-Report_v1.2.md).

## Contents

| File | What it is |
|---|---|
| `CLAIM_REGISTRATION.md` | The claim as frozen on 2026-08-16, unmodified. It does not describe the split-half test that was run; the report's §7.2 explains the deviation. |
| `reproduce_assay002.py` | Reproduces every number in the report from the public data. |
| `results/session-2026-08-16/` | Outputs from the original analysis session. |
| `results/reproduction_2026-09-24.json` | Output of the script run fresh against the pinned inputs. |

## Reproduce

```bash
git clone https://github.com/Mcompetitions/M6-methods.git
git -C M6-methods checkout 10c553f7a5ffbaf53971ca48ea982b2c0dd952ed
pip install numpy pandas scipy openpyxl
python reproduce_assay002.py M6-methods
```

The script checks SHA-256 hashes of the three input files before computing and stops on any mismatch. Seed 20260816 throughout. Runtime is a few minutes on a laptop. Verified 2026-09-24 with numpy 2.4.4, pandas 3.0.2, scipy 1.17.1, openpyxl 3.1.5.

## Credit

The data and the forecast-versus-investment question belong to the M6 organizers: Makridakis, Spiliotis, Hollyman, Petropoulos, Swanson & Gaba, "The M6 forecasting competition: Bridging the gap between forecasting and investment decisions," *International Journal of Forecasting* 41(4), 2025.

## License

Code (`reproduce_assay002.py`) is released under the [MIT License](LICENSE). The report, the claim registration, and the files in `results/` are released under [CC BY 4.0](LICENSE-CC-BY-4.0.txt). The M6 competition data is not included here; it belongs to the M6 organizers and is fetched from their repository.
