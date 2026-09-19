import { cohortPlan, cohortSize, newlyReached } from "../cohort/cohorts.js";
import { planRollout } from "../rollout/schedule.js";
import type { Device, Rollout } from "../rollout/types.js";

export interface PlanRequest {
  rollout: Rollout;
  devices: Device[];
}

export function postPlan(body: PlanRequest) {
  const enrolments = planRollout(body.devices, body.rollout);
  const ids = body.devices.map((d) => d.id);
  return {
    rollout: body.rollout.id,
    enrolled: enrolments.filter((e) => !e.heldBack).length,
    heldBack: enrolments.filter((e) => e.heldBack).length,
    cohorts: cohortPlan(ids, body.rollout.stages).map((cohort) => ({
      stage: cohort.stage,
      reachPercent: cohort.reachPercent,
      size: cohort.members.length,
    })),
    enrolments,
  };
}

/** Preview what widening a stage would admit, without enrolling anything. */
export function getCohortPreview(body: PlanRequest, stageName: string) {
  const ids = body.devices.map((d) => d.id);
  const stages = body.rollout.stages;
  const index = stages.findIndex((s) => s.name === stageName);
  if (index < 0) {
    throw new RangeError(`no stage named ${stageName}`);
  }
  const previous = index === 0 ? 0 : stages[index - 1]!.reachPercent;
  const target = stages[index]!.reachPercent;
  return {
    stage: stageName,
    from: previous,
    to: target,
    currentSize: cohortSize(ids, previous),
    targetSize: cohortSize(ids, target),
    newlyReached: newlyReached(ids, previous, target).length,
  };
}
