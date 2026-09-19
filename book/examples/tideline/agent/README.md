# tideline

Stages firmware rollouts to field devices.

## Running it

```
npm ci
npm test
```

## Layout

- `src/cohort/` — device-to-bucket assignment and percentage-gated cohorts
- `src/rollout/` — stage planning and eligibility
- `src/api/` — the HTTP surface

## Rollout stages

Each stage carries a `reachPercent`. A rollout typically widens 5 → 25 → 50 →
100 across successive stages.

Two invariants hold, and both are enforced in `src/cohort/cohorts.ts`:

- **Assignment is stable.** A device identifier maps to the same bucket in every
  process and every release, so re-planning a rollout does not reshuffle who is
  in the early waves.
- **Widening is monotonic.** A device inside the 5 per cent cohort is inside the
  25 per cent cohort. `assertWidening` rejects a stage list that narrows, because
  the device-side agent has no way to honour a device being taken back out.

`GET /rollouts/:id/cohorts/:stage` previews what widening a stage would admit
before anything is enrolled.
