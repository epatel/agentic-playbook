import assert from "node:assert/strict";
import { describe, it } from "node:test";

import { planStage, hasBatteryFor } from "../src/rollout/schedule.js";
import type { Device, Rollout, RolloutStage } from "../src/rollout/types.js";

const stage: RolloutStage = { name: "canary", minBatteryPercent: 40 };

const rollout: Rollout = {
  id: "r-2026-09",
  firmware: "4.2.0",
  stages: [stage],
};

function device(id: string, batteryPercent: number): Device {
  return {
    id,
    model: "tide-2",
    firmware: "4.1.0",
    batteryPercent,
    lastSeen: "2026-09-18T04:00:00Z",
  };
}

describe("rollout scheduling", () => {
  it('holds back devices below the minimum battery threshold', async () => {
    const out = planStage([device("dev-001", 12)], rollout, stage);
    assert.equal(out.length, 1);
    assert.equal(out[0]?.heldBack, true);
    assert.equal(out[0]?.reason, "battery");
  });

  it("enrols devices above the threshold", async () => {
    const out = planStage([device("dev-002", 90)], rollout, stage);
    assert.equal(out[0]?.heldBack, false);
  });

  it("skips devices already on the target firmware", async () => {
    const already = { ...device("dev-003", 90), firmware: "4.2.0" };
    const out = planStage([already], rollout, stage);
    assert.equal(out.length, 0);
  });

  it("treats the threshold as inclusive", async () => {
    assert.equal(hasBatteryFor(device("dev-004", 40), stage), true);
    assert.equal(hasBatteryFor(device("dev-005", 39), stage), false);
  });
});
