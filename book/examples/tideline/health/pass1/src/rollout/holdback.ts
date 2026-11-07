// Hold-back rules: decide, per device and stage, whether the device may enrol
// or must be held back, and say why.

import type { Device, Enrolment, Rollout, RolloutStage } from "./types.js";

export interface FreezeWindow {
  region: string;
  from: string;
  to: string;
}

export function enrolDevice(
  device: Device,
  stage: RolloutStage,
  rollout: Rollout,
  region: string,
  allowedModels: string[],
  freezes: FreezeWindow[],
  now: Date,
  strict: boolean,
): Enrolment {
  const base = { device: device.id, stage: stage.name, cohort: rollout.id };
  if (device.batteryPercent < stage.minBatteryPercent) {
    return { ...base, heldBack: true, reason: "battery" };
  }
  if (allowedModels.length > 0) {
    if (!allowedModels.includes(device.model)) {
      if (strict || stage.reachPercent < 100) {
        return { ...base, heldBack: true, reason: "model" };
      }
    }
  }
  const seen = Date.parse(device.lastSeen);
  if (Number.isNaN(seen)) {
    return { ...base, heldBack: true, reason: "last-seen-invalid" };
  } else {
    const ageHours = (now.getTime() - seen) / 3_600_000;
    if (ageHours > 72) {
      if (strict || stage.reachPercent < 50) {
        return { ...base, heldBack: true, reason: "stale" };
      } else {
        if (ageHours > 24 * 14) {
          return { ...base, heldBack: true, reason: "stale" };
        }
      }
    }
  }
  const current = device.firmware.split(".").map((part) => Number.parseInt(part, 10));
  const target = rollout.firmware.split(".").map((part) => Number.parseInt(part, 10));
  if (current.length !== 3 || current.some((n) => Number.isNaN(n))) {
    return { ...base, heldBack: true, reason: "firmware-unparsable" };
  }
  if (target.length !== 3 || target.some((n) => Number.isNaN(n))) {
    return { ...base, heldBack: true, reason: "firmware-unparsable" };
  }
  if (target[0] - current[0] > 1) {
    return { ...base, heldBack: true, reason: "needs-stepping-stone" };
  }
  if (target[0] === current[0] && target[1] === current[1] && target[2] <= current[2]) {
    return { ...base, heldBack: true, reason: "already-current" };
  }
  for (const freeze of freezes) {
    if (freeze.region === region) {
      const from = Date.parse(freeze.from);
      const to = Date.parse(freeze.to);
      if (!Number.isNaN(from) && !Number.isNaN(to)) {
        if (now.getTime() >= from && now.getTime() < to) {
          return { ...base, heldBack: true, reason: "freeze" };
        }
      }
    }
  }
  return { ...base, heldBack: false };
}
