"""Stateful high-level brain for the simulated robotic dog.

The brain is intentionally deterministic and auditable. It is not an LLM,
vision model, trained policy, or safety-certified controller.
"""
from dataclasses import dataclass

from .behavior import BehaviorController, RobotState, SensorSnapshot
from .memory import EpisodicMemory


@dataclass(frozen=True)
class BrainDecision:
    state: RobotState
    goal: str
    mood: str
    explanation: str
    memory_count: int


class DogBrain:
    """Combine priorities, simple companion personality, goals, and episodic memory."""

    def __init__(self, low_battery_threshold: float = 10.0) -> None:
        self.controller = BehaviorController(low_battery_threshold)
        self.memory = EpisodicMemory()
        self._last_state: RobotState | None = None
        self._interaction_count = 0

    def think(self, observation: SensorSnapshot) -> BrainDecision:
        state = self.controller.decide(observation)

        if state is RobotState.STOPPED:
            goal, mood, explanation = "stop_and_wait", "calm", "An explicit stop command has top priority."
        elif state is RobotState.RETURN_TO_CHARGE:
            goal, mood, explanation = "find_charging_station", "careful", "Battery is at or below the configured threshold."
        elif state is RobotState.AVOID_OBSTACLE:
            goal, mood, explanation = "choose_clear_path", "alert", "An obstacle was reported; movement must be handled by a separate planner."
        elif state is RobotState.COMPANION:
            goal, mood, explanation = "engage_companion", "friendly", "A person was detected; companion interaction is appropriate."
            self._interaction_count += 1
        else:
            goal, mood, explanation = "explore_safely", "curious", "No higher-priority event was reported."

        if state != self._last_state:
            self.memory.remember("state_change", f"{self._last_state or 'start'} -> {state.value}")
        if state is RobotState.COMPANION:
            self.memory.remember("person_detected", f"companion interaction #{self._interaction_count}")
        if observation.obstacle_detected:
            self.memory.remember("obstacle", "obstacle detected in current observation")

        self._last_state = state
        return BrainDecision(
            state=state,
            goal=goal,
            mood=mood,
            explanation=explanation,
            memory_count=self.memory.count(),
        )
