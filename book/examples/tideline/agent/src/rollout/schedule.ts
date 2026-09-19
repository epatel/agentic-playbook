import { hashToBucket } from "../cohort/cohorts.js";
import type { Device, Enrolment, Rollout, RolloutStage } from "./types.js";

/** A device is eligible for a stage if it has the battery to survive the flash. */
export function hasBatteryFor(device: Device, stage: RolloutStage): boolean {
  return device.batteryPercent >= stage.minBatteryPercent;
}

/** A device already on the target firmware has nothing to do. */
export function needsFirmware(device: Device, rollout: Rollout): boolean {
  return device.firmware !== rollout.firmware;
}

/** True when the device's bucket falls inside the stage's percentage gate. */
export function withinReach(device: Device, stage: RolloutStage): boolean {
  if (stage.reachPercent >= 100) {
    return true;
  }
  return hashToBucket(device.id, 100) < stage.reachPercent;
}

/**
 * Plan one stage of a rollout.
 *
 * Devices are assigned to a cohort first, so that the percentage gate is
 * computed once per stage and the enrolment record carries the cohort it
 * landed in.
 */
export function planStage(
  devices: Device[],
  rollout: Rollout,
  stage: RolloutStage,
): Enrolment[] {
  const out: Enrolment[] = [];
  for (const device of devices) {
    if (!needsFirmware(device, rollout)) {
      continue;
    }
    const cohort = `${stage.name}@${stage.reachPercent}`;
    if (!withinReach(device, stage)) {
      out.push({
        device: device.id,
        stage: stage.name,
        cohort,
        heldBack: true,
        reason: "out-of-cohort",
      });
      continue;
    }
    if (!hasBatteryFor(device, stage)) {
      out.push({
        device: device.id,
        stage: stage.name,
        cohort,
        heldBack: true,
        reason: "battery",
      });
      continue;
    }
    out.push({ device: device.id, stage: stage.name, cohort, heldBack: false });
  }
  return out;
}

export function planRollout(devices: Device[], rollout: Rollout): Enrolment[] {
  return rollout.stages.flatMap((stage) => planStage(devices, rollout, stage));
}
