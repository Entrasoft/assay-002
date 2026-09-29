# Assay No. 002 — Claim Registration

**Registered:** 2026-08-16, prior to any data access in this session.

**Subject:** M6 Financial Forecasting & Investment Competition (Mcompetitions/M6-methods),
public submissions dataset.

**Registered claim:**
> "Top-ranked M6 performance is distinguishable from luck after multiplicity
> correction across the full 251-team population."

**Protocol (fixed before analysis):**
1. Load the full public submissions population. No filtering on activity status,
   submission count, or performance prior to analysis.
2. Define the primary outcome metric as-used by the competition organizers
   (RPS-based ranking for the forecasting track; IR-based for the investment
   track) using the data's own hash-verifiable fields where possible.
3. Compute each team's realized performance rank.
4. Test: is the top-ranked team's (or top-decile's) performance distinguishable
   from the performance expected under a null model where all 251 teams are
   equally skilled (i.e., rankings are exchangeable / random)?
5. Apply multiplicity correction appropriate to a 251-way comparison (family-wise
   or FDR control) rather than treating the top performer's p-value as if it were
   the only test run.
6. Rejects-in-denominator rule: all 251 teams that ever submitted are the
   population of record, including inactive/trial-only entrants, unless a
   documented reason excludes a team (documented in §1.3 as a scope note, not
   silently dropped).
7. Single-shot: this analysis runs once against this protocol. If the protocol
   needs revision after seeing results, that revision is logged as a protocol
   violation and the report is capped at "Supported with conditions" per
   schema §7.5.

**Verdict enum (schema v0.1):** Supported / Supported with conditions /
Not supported / Not evaluable.

**What would falsify "Supported":** if, after multiplicity correction, the
probability of observing the top performer's rank under the null (all-skill-
equal) model is not small (i.e., consistent with luck), the claim is Not
supported — regardless of how impressive the raw ranking looks.
