export type DeviceId = string;

export interface Device {
  id: DeviceId;
  model: string;
  firmware: string;
  batteryPercent: number;
  lastSeen: string;
}

export interface RolloutStage {
  name: string;
  minBatteryPercent: number;
  /** Per cent of the fleet this stage may reach. 100 means everything. */
  reachPercent: number;
}

export interface Cohort {
  stage: string;
  reachPercent: number;
  members: DeviceId[];
}

export interface Rollout {
  id: string;
  firmware: string;
  stages: RolloutStage[];
}

export interface Enrolment {
  device: DeviceId;
  stage: string;
  cohort: string;
  heldBack: boolean;
  reason?: string;
}
