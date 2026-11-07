// Hold-back rules: decide, per device and stage, whether the device may enrol
// or must be held back, and say why. Each rule returns a reason or null; the
// first reason wins.

import type { Device, Enrolment, Rollout, RolloutStage } from "./types.js";

export interface FreezeWindow {
  region: string;
  from: string;
  to: string;
}

export interface HoldbackContext {
  stage: RolloutStage;
  rollout: Rollout;
  region: string;
  allowedModels: string[];
  freezes: FreezeWindow[];
  now: Date;
  strict: boolean;
}

type Rule = (device: Device, ctx: HoldbackContext) => string | null;

const HOUR_MS = 3_600_000;
const STALE_HOURS = 72;
const STALE_HOURS_WIDE = 24 * 14;

function isNarrow(ctx: HoldbackContext, belowPercent: number): boolean {
  return ctx.strict || ctx.stage.reachPercent < belowPercent;
}

function parseVersion(version: string): number[] | null {
  const parts = version.split(".").map((part) => Number.parseInt(part, 10));
  return parts.length === 3 && !parts.some(Number.isNaN) ? parts : null;
}

const battery: Rule = (device, ctx) =>
  device.batteryPercent < ctx.stage.minBatteryPercent ? "battery" : null;

const model: Rule = (device, ctx) => {
  const listed = ctx.allowedModels.length === 0 || ctx.allowedModels.includes(device.model);
  return listed || !isNarrow(ctx, 100) ? null : "model";
};

const staleness: Rule = (device, ctx) => {
  const seen = Date.parse(device.lastSeen);
  if (Number.isNaN(seen)) {
    return "last-seen-invalid";
  }
  const ageHours = (ctx.now.getTime() - seen) / HOUR_MS;
  const limit = isNarrow(ctx, 50) ? STALE_HOURS : STALE_HOURS_WIDE;
  return ageHours > limit ? "stale" : null;
};

const firmware: Rule = (device, ctx) => {
  const current = parseVersion(device.firmware);
  const target = parseVersion(ctx.rollout.firmware);
  if (current === null || target === null) {
    return "firmware-unparsable";
  }
  if (target[0] - current[0] > 1) {
    return "needs-stepping-stone";
  }
  const sameMinor = target[0] === current[0] && target[1] === current[1];
  return sameMinor && target[2] <= current[2] ? "already-current" : null;
};

function inWindow(freeze: FreezeWindow, now: Date): boolean {
  const from = Date.parse(freeze.from);
  const to = Date.parse(freeze.to);
  return now.getTime() >= from && now.getTime() < to;
}

const freeze: Rule = (_device, ctx) =>
  ctx.freezes.some((f) => f.region === ctx.region && inWindow(f, ctx.now)) ? "freeze" : null;

const RULES: readonly Rule[] = [battery, model, staleness, firmware, freeze];

export function enrolDevice(device: Device, ctx: HoldbackContext): Enrolment {
  const base = { device: device.id, stage: ctx.stage.name, cohort: ctx.rollout.id };
  for (const rule of RULES) {
    const reason = rule(device, ctx);
    if (reason !== null) {
      return { ...base, heldBack: true, reason };
    }
  }
  return { ...base, heldBack: false };
}
