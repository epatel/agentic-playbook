import assert from "node:assert/strict";
import { describe, it } from "node:test";

import {
  assertWidening,
  cohortMembers,
  cohortPlan,
  cohortSize,
  hashToBucket,
  newlyReached,
  withinReachPercent,
  STANDARD_REACH,
} from "../src/cohort/cohorts.js";
import type { RolloutStage } from "../src/rollout/types.js";

const fleet = Array.from({ length: 1000 }, (_, i) => `dev-${String(i).padStart(4, "0")}`);

function stage(name: string, reachPercent: number): RolloutStage {
  return { name, minBatteryPercent: 40, reachPercent };
}

describe("bucket assignment", () => {
  it("is stable across calls", async () => {
    assert.equal(hashToBucket("dev-0042", 100), hashToBucket("dev-0042", 100));
  });

  it("keeps every bucket inside range", async () => {
    for (const id of fleet.slice(0, 200)) {
      const bucket = hashToBucket(id, 100);
      assert.ok(bucket >= 0 && bucket < 100, `${id} -> ${bucket}`);
    }
  });

  it("rejects a non-positive bucket count", async () => {
    assert.throws(() => hashToBucket("dev-0001", 0), RangeError);
    assert.throws(() => hashToBucket("dev-0001", -1), RangeError);
  });

  it("spreads a thousand devices over most of the buckets", async () => {
    const seen = new Set(fleet.map((id) => hashToBucket(id, 100)));
    assert.ok(seen.size > 80, `expected a wide spread, got ${seen.size} buckets`);
  });
});

describe("percentage-gated cohorts", () => {
  it("returns the whole fleet at 100 per cent", async () => {
    assert.equal(cohortSize(fleet, 100), fleet.length);
  });

  it("returns nothing at zero per cent", async () => {
    assert.equal(cohortSize(fleet, 0), 0);
  });

  it("reaches roughly five per cent of the fleet at a five per cent gate", async () => {
    const size = cohortSize(fleet, 5);
    assert.ok(size > 20 && size < 80, `expected roughly 50, got ${size}`);
  });

  it("widens monotonically", async () => {
    const five = new Set(cohortMembers(fleet, 5));
    const twentyFive = new Set(cohortMembers(fleet, 25));
    for (const id of five) {
      assert.ok(twentyFive.has(id), `${id} fell out of the wider cohort`);
    }
  });

  it("agrees with the single-device predicate", async () => {
    const members = new Set(cohortMembers(fleet, 25));
    for (const id of fleet.slice(0, 100)) {
      assert.equal(members.has(id), withinReachPercent(id, 25));
    }
  });

  it("reports only the devices a widening step newly admits", async () => {
    const added = newlyReached(fleet, 5, 25);
    const five = new Set(cohortMembers(fleet, 5));
    for (const id of added) {
      assert.ok(!five.has(id), `${id} was already in the narrower cohort`);
    }
    assert.equal(added.length, cohortSize(fleet, 25) - cohortSize(fleet, 5));
  });
});

describe("rollout plans", () => {
  it("builds one cohort per stage, in widening order", async () => {
    const stages = STANDARD_REACH.map((p) => stage(`wave-${p}`, p));
    const plan = cohortPlan(fleet, stages);
    assert.equal(plan.length, stages.length);
    for (let i = 1; i < plan.length; i++) {
      assert.ok(plan[i]!.members.length >= plan[i - 1]!.members.length);
    }
  });

  it("rejects a stage list that narrows", async () => {
    assert.throws(() => assertWidening([stage("a", 25), stage("b", 5)]), RangeError);
  });

  it("accepts a stage list that repeats a percentage", async () => {
    assert.doesNotThrow(() => assertWidening([stage("a", 25), stage("b", 25)]));
  });
});
