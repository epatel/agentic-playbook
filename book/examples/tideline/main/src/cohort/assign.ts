// Cohort assignment for staged firmware rollouts.
//
// A device is assigned to a stable bucket derived from its identifier, so that
// re-running a rollout plan does not reshuffle which devices are in the early
// waves. The hash is deliberately boring: we need stability across processes
// and releases, not cryptographic strength.

const FNV_OFFSET = 2166136261;
const FNV_PRIME = 16777619;

/** Stable 32-bit FNV-1a over the device identifier. */
export function hashDeviceId(deviceId: string): number {
  let h = FNV_OFFSET;
  for (let i = 0; i < deviceId.length; i++) {
    h ^= deviceId.charCodeAt(i);
    h = Math.imul(h, FNV_PRIME);
  }
  return h >>> 0;
}

/**
 * Assign a device to one of `buckets` buckets, numbered from 0.
 *
 * Tie-break at the boundary is deliberate: a device whose hash lands exactly on
 * a bucket edge goes to the LOWER bucket, so widening a rollout never moves a
 * device backwards out of a wave it has already entered.
 */
export function bucketFor(deviceId: string, buckets: number): number {
  if (buckets <= 0) {
    throw new RangeError(`buckets must be positive, got ${buckets}`);
  }
  const h = hashDeviceId(deviceId);
  const bucket = Math.floor((h / 0x100000000) * buckets);
  return Math.min(bucket, buckets - 1);
}

/** True when the device falls inside the first `percent` per cent of buckets. */
export function withinPercent(deviceId: string, percent: number): boolean {
  if (percent <= 0) return false;
  if (percent >= 100) return true;
  return bucketFor(deviceId, 100) < percent;
}
