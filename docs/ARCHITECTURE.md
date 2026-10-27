# Initial Architecture

## Design approach

The project starts with a software-first architecture so behavior can be developed and tested before any physical robot is available.

```text
Sensor / Perception Adapters (future)
              |
              v
      SensorSnapshot
              |
              v
     BehaviorController
              |
              v
        RobotState
              |
              v
Simulation / Motion Planner (future; not implemented)
```

## Implemented today

- `SensorSnapshot`: immutable, normalized input values for a single decision.
- `BehaviorController`: deterministic rules with a configurable low-battery threshold.
- `RobotState`: high-level state labels.
- `tests/test_behavior.py`: tests for priority rules and input validation.
- `python -m dog_robot_ai`: a demo using synthetic observations.

## Explicit limitations

- No camera, microphone, motor, battery sensor, or robot hardware integration exists yet.
- The demo uses synthetic inputs, not live sensor readings.
- `AVOID_OBSTACLE` is a requested high-level state, not an implemented avoidance trajectory.
- `RETURN_TO_CHARGE` is a requested high-level state, not navigation or docking logic.
- The controller is not safety-certified and must not be connected directly to actuators.

## Planned modules

1. **Simulation:** a separate optional MuJoCo environment and robot model.
2. **Perception:** replaceable interfaces for camera and other sensor outputs.
3. **Planning and motion:** simulated locomotion, collision checks, and explicit command limits.
4. **Companion behavior:** configurable interaction states and privacy-aware sensing.
5. **Local AI adapters:** optional interfaces to locally hosted models without making the core package depend on one model vendor.
6. **Observability:** structured logs, reproducible scenarios, and regression tests.

## Safety development rule

No physical actuator integration should be considered until simulation tests, bounded commands, emergency-stop behavior, and hardware-specific safety mechanisms have been separately designed and reviewed.
