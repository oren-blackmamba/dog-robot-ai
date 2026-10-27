"""Run a short demonstration with synthetic observations."""

from .behavior import BehaviorController, SensorSnapshot


def main() -> None:
    controller = BehaviorController()
    examples = [
        ("No activity", SensorSnapshot()),
        ("Person detected", SensorSnapshot(person_detected=True)),
        ("Obstacle detected", SensorSnapshot(obstacle_detected=True)),
        ("Battery low", SensorSnapshot(battery_percent=8.0)),
        ("Stop requested", SensorSnapshot(person_detected=True, command="stop")),
    ]
    for label, observation in examples:
        print(f"{label:20} -> {controller.decide(observation).value}")


if __name__ == "__main__":
    main()
