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
}

export interface Rollout {
  id: string;
  firmware: string;
  stages: RolloutStage[];
}

export interface Enrolment {
  device: DeviceId;
  stage: string;
  heldBack: boolean;
  reason?: string;
}
