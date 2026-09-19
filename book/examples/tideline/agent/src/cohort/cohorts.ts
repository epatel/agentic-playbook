// Percentage-gated cohorts for staged rollouts.
//
// A cohort is the slice of the fleet a stage is allowed to reach. Stages widen
// over the life of a rollout: 5 per cent, then 25, then everything. Two rules
// hold across the whole lifecycle, and both are tested in tests/cohort.spec.ts:
//
//   1. Assignment is stable. The same device identifier always lands in the
//      same bucket, in this process and in the next one.
//   2. Widening is monotonic. A device inside a 5 per cent cohort is still
//      inside the 25 per cent cohort. Nothing ever falls back out.

import type { Cohort, DeviceId, RolloutStage } from "../rollout/types.js";

const OFFSET = 2166136261;
const PRIME = 16777619;

/** The reach percentages a rollout is allowed to use, in widening order. */
export const STANDARD_REACH: readonly number[] = [5, 25, 50, 100];

/** 32-bit FNV-1a over an identifier. */
function hash32(id: string): number {
  let h = OFFSET;
  for (let i = 0; i < id.length; i++) {
    h ^= id.charCodeAt(i);
    h = Math.imul(h, PRIME);
  }
  return h >>> 0;
}

/**
 * Map an identifier onto one of `n` buckets.
 *
 * Boundary devices round UP into the higher bucket, which keeps the split even
 * when n does not divide the hash space cleanly.
 */
export function hashToBucket(id: string, n: number): number {
  if (n <= 0) {
    throw new RangeError(`n must be positive, got ${n}`);
  }
  const h = hash32(id);
  const scaled = (h / 0x100000000) * n;
  const bucket = Math.ceil(scaled) - 1;
  return bucket < 0 ? 0 : Math.min(bucket, n - 1);
}

/** True when a device's bucket falls inside a reach percentage. */
export function withinReachPercent(id: DeviceId, reachPercent: number): boolean {
  if (reachPercent >= 100) {
    return true;
  }
  if (reachPercent <= 0) {
    return false;
  }
  return hashToBucket(id, 100) < reachPercent;
}

/** The devices a stage at `reachPercent` may touch. */
export function cohortMembers(ids: DeviceId[], reachPercent: number): DeviceId[] {
  if (reachPercent >= 100) {
    return [...ids];
  }
  if (reachPercent <= 0) {
    return [];
  }
  return ids.filter((id) => withinReachPercent(id, reachPercent));
}

/** How many devices a reach percentage works out to, for the plan preview. */
export function cohortSize(ids: DeviceId[], reachPercent: number): number {
  return cohortMembers(ids, reachPercent).length;
}

/** Build the cohort record a stage will be planned against. */
export function cohortFor(ids: DeviceId[], stage: RolloutStage): Cohort {
  return {
    stage: stage.name,
    reachPercent: stage.reachPercent,
    members: cohortMembers(ids, stage.reachPercent),
  };
}

/**
 * Reject a stage list that narrows.
 *
 * A rollout whose stages go 25 then 5 would take devices back out of a cohort
 * they had already entered, which the device-side agent has no way to honour.
 */
export function assertWidening(stages: RolloutStage[]): void {
  let previous = 0;
  for (const stage of stages) {
    if (stage.reachPercent < previous) {
      throw new RangeError(
        `stage ${stage.name} narrows from ${previous} to ${stage.reachPercent}`,
      );
    }
    previous = stage.reachPercent;
  }
}

/** The successive cohorts of a whole rollout, for the plan preview. */
export function cohortPlan(ids: DeviceId[], stages: RolloutStage[]): Cohort[] {
  assertWidening(stages);
  return stages.map((stage) => cohortFor(ids, stage));
}

/** Devices that enter at this stage and were not in the previous one. */
export function newlyReached(
  ids: DeviceId[],
  previousPercent: number,
  reachPercent: number,
): DeviceId[] {
  const already = new Set(cohortMembers(ids, previousPercent));
  return cohortMembers(ids, reachPercent).filter((id) => !already.has(id));
}
