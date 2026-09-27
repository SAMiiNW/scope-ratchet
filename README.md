# SCOPE RATCHET

> A change order is not small when the previous nine are still on the ledger.

## The gauge

`Scope Ratchet` freezes a procurement rulebook and award, then measures later change orders in basis points. Validators agree on bounded impact, scope code, trigger mask, and source digests; the contract converts those fields into readable scope, indexes, and a deterministic summary. The contract computes materiality itself. A `NEW` scope, one oversized order, or a cumulative total at the threshold produces `RETENDER_REQUIRED`.

The total only moves forward after a review window closes. An independent oversight wallet may attach a fresh-origin challenge and force validators to recompute the measurement. Anyone may finalize after the clock; the buyer cannot hide a matured result.

```text
OPEN
  contractor files an order
ORDER_UNDER_REVIEW
  oversight may challenge the measurement
APPROVED -> OPEN with a higher cumulative gauge
RETENDER_REQUIRED -> terminal stop
```

## Instrument tolerances

- Three distinct wallets: buyer, contractor, oversight.
- Rulebook and award must use different HTTPS origins.
- Frozen source bytes are digest-checked on every measurement.
- Impact is bounded to `0..10000` basis points.
- Scope class is closed to `SAME / ADJACENT / NEW`.
- Rule indexes are unique, sorted, and range-checked.
- Demo files are operator-created technical fixtures, not independent procurement authorities.

## Bench command

`evidence/live-proof.json` records the StudioNet run where 600 approved basis points plus a 450-basis-point order produced a 1050-basis-point projection and the terminal `RETENDER_REQUIRED` state.

```bash
genvm-lint contracts/contract.py
python -m pytest tests/test_surface.py -q
python -m pytest tests/direct -q
```

The direct suite covers roles, cumulative thresholds, challenges, mutated frozen sources, and a forged leader impact. On the current Windows `gltest` build, direct collection is blocked by the SDK loader error `unexpected end of memory`; the recorded StudioNet lifecycle remains the authoritative execution proof.
