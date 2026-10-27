import unittest

from dog_robot_ai.behavior import BehaviorController, RobotState, SensorSnapshot


class BehaviorControllerTests(unittest.TestCase):
    def setUp(self):
        self.controller = BehaviorController()

    def test_defaults_to_idle(self):
        self.assertEqual(self.controller.decide(SensorSnapshot()), RobotState.IDLE)

    def test_person_detection_selects_companion(self):
        self.assertEqual(
            self.controller.decide(SensorSnapshot(person_detected=True)),
            RobotState.COMPANION,
        )

    def test_obstacle_has_priority_over_person(self):
        observation = SensorSnapshot(obstacle_detected=True, person_detected=True)
        self.assertEqual(
            self.controller.decide(observation), RobotState.AVOID_OBSTACLE
        )

    def test_low_battery_has_priority_over_obstacle(self):
        observation = SensorSnapshot(
            battery_percent=5, obstacle_detected=True, person_detected=True
        )
        self.assertEqual(
            self.controller.decide(observation), RobotState.RETURN_TO_CHARGE
        )

    def test_stop_has_highest_priority(self):
        observation = SensorSnapshot(
            battery_percent=1, obstacle_detected=True, command=" STOP "
        )
        self.assertEqual(self.controller.decide(observation), RobotState.STOPPED)

    def test_battery_threshold_is_inclusive(self):
        self.assertEqual(
            self.controller.decide(SensorSnapshot(battery_percent=10)),
            RobotState.RETURN_TO_CHARGE,
        )

    def test_rejects_battery_outside_range(self):
        with self.assertRaises(ValueError):
            SensorSnapshot(battery_percent=101)

    def test_rejects_invalid_threshold(self):
        with self.assertRaises(ValueError):
            BehaviorController(low_battery_threshold=-1)


if __name__ == "__main__":
    unittest.main()
