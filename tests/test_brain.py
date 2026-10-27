import unittest

from dog_robot_ai.behavior import RobotState, SensorSnapshot
from dog_robot_ai.brain import DogBrain


class DogBrainTests(unittest.TestCase):
    def test_person_detection_creates_friendly_goal(self):
        brain = DogBrain()
        decision = brain.think(SensorSnapshot(person_detected=True))
        self.assertEqual(decision.state, RobotState.COMPANION)
        self.assertEqual(decision.goal, "engage_companion")
        self.assertEqual(decision.mood, "friendly")
        self.assertGreater(decision.memory_count, 0)

    def test_stop_overrides_other_events(self):
        decision = DogBrain().think(SensorSnapshot(
            battery_percent=1, obstacle_detected=True, person_detected=True, command="STOP"
        ))
        self.assertEqual(decision.state, RobotState.STOPPED)
        self.assertEqual(decision.goal, "stop_and_wait")

    def test_low_battery_overrides_obstacle(self):
        decision = DogBrain().think(SensorSnapshot(battery_percent=5, obstacle_detected=True))
        self.assertEqual(decision.state, RobotState.RETURN_TO_CHARGE)

    def test_obstacle_goal_is_not_a_motor_command(self):
        decision = DogBrain().think(SensorSnapshot(obstacle_detected=True))
        self.assertEqual(decision.goal, "choose_clear_path")
        self.assertIn("separate planner", decision.explanation)

    def test_memory_is_bounded(self):
        brain = DogBrain()
        for i in range(150):
            brain.think(SensorSnapshot(command="stop" if i % 2 else "idle"))
        self.assertLessEqual(brain.memory.count(), 100)


if __name__ == "__main__":
    unittest.main()
