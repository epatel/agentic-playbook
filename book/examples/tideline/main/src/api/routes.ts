import { planRollout } from "../rollout/schedule.js";
import type { Device, Rollout } from "../rollout/types.js";

export interface PlanRequest {
  rollout: Rollout;
  devices: Device[];
}

export function postPlan(body: PlanRequest) {
  const enrolments = planRollout(body.devices, body.rollout);
  return {
    rollout: body.rollout.id,
    enrolled: enrolments.filter((e) => !e.heldBack).length,
    heldBack: enrolments.filter((e) => e.heldBack).length,
    enrolments,
  };
}
