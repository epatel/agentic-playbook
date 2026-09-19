# tideline

Stages firmware rollouts to field devices.

## Running it

```
npm ci
npm test
npm run typecheck
```

## Layout

- `src/cohort/` — device-to-bucket assignment
- `src/rollout/` — stage planning and eligibility
- `src/api/` — the HTTP surface
