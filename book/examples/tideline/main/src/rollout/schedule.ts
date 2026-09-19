import type { Device, Enrolment, Rollout, RolloutStage } from "./types.js";

/** A device is eligible for a stage if it has the battery to survive the flash. */
export function hasBatteryFor(device: Device, stage: RolloutStage): boolean {
  return device.batteryPercent >= stage.minBatteryPercent;
}

/** A device already on the target firmware has nothing to do. */
export function needsFirmware(device: Device, rollout: Rollout): boolean {
  return device.firmware !== rollout.firmware;
}

/**
 * Plan one stage of a rollout.
 *
 * Order matters: the battery check runs before anything else, so a device that
 * cannot take the flash is never enrolled in the first place.
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
    if (!hasBatteryFor(device, stage)) {
      out.push({
        device: device.id,
        stage: stage.name,
        heldBack: true,
        reason: "battery",
      });
      continue;
    }
    out.push({ device: device.id, stage: stage.name, heldBack: false });
  }
  return out;
}

export function planRollout(devices: Device[], rollout: Rollout): Enrolment[] {
  return rollout.stages.flatMap((stage) => planStage(devices, rollout, stage));
}
