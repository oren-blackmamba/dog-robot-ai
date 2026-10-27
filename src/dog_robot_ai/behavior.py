"""Small, deterministic behavior layer for the Dog Robot AI prototype.

This module selects high-level states only. It does not generate gait,
trajectory, or motor commands and is not a real-world safety controller.
"""

from dataclasses import dataclass
from enum import Enum


class RobotState(str, Enum):
    """High-level behavior states used by the prototype."""

    IDLE = "idle"
    COMPANION = "companion"
    AVOID_OBSTACLE = "avoid_obstacle"
    RETURN_TO_CHARGE = "return_to_charge"
    STOPPED = "stopped"


@dataclass(frozen=True)
class SensorSnapshot:
    """Minimal normalized observation supplied to the behavior controller."""

    battery_percent: float = 100.0
    obstacle_detected: bool = False
    person_detected: bool = False
    command: str = "idle"

    def __post_init__(self) -> None:
        if not 0.0 <= self.battery_percent <= 100.0:
            raise ValueError("battery_percent must be between 0 and 100")
        if not isinstance(self.command, str):
            raise TypeError("command must be a string")


class BehaviorController:
    """Choose a high-level state using explicit, testable priority rules."""

    def __init__(self, low_battery_threshold: float = 10.0) -> None:
        if not 0.0 <= low_battery_threshold <= 100.0:
            raise ValueError("low_battery_threshold must be between 0 and 100")
        self.low_battery_threshold = low_battery_threshold

    def decide(self, observation: SensorSnapshot) -> RobotState:
        """Return the next requested state: stop, charge, avoid, companion, or idle."""
        if observation.command.strip().lower() == "stop":
            return RobotState.STOPPED
        if observation.battery_percent <= self.low_battery_threshold:
            return RobotState.RETURN_TO_CHARGE
        if observation.obstacle_detected:
            return RobotState.AVOID_OBSTACLE
        if observation.person_detected:
            return RobotState.COMPANION
        return RobotState.IDLE
