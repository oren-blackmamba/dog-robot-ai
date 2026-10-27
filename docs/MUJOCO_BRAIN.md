# Dog AI Brain + MuJoCo

## What is connected

- `DogBrain` converts a normalized `SensorSnapshot` into a high-level state, goal, mood label, explanation, and memory count.
- `EpisodicMemory` keeps a bounded in-process history of recent state changes and events.
- `simulation/dog_quadruped.xml` defines a simple four-legged articulated model for MuJoCo.
- `mujoco_sim.py` loads that model, advances the physics engine, and feeds scripted test events into the brain.

## Install and run

Python 3.10 or newer is required.

```bash
python -m pip install -e ".[simulation]"
PYTHONPATH=src python -m dog_robot_ai.mujoco_sim
PYTHONPATH=src python -m unittest discover -s tests -v
```

On Windows PowerShell, set the source path first:

```powershell
$env:PYTHONPATH = "src"
python -m dog_robot_ai.mujoco_sim
python -m unittest discover -s tests -v
```

The viewer requires a desktop graphics session. The model can also be loaded headlessly by calling `run_demo(show_viewer=False)`.

## Brain design

The current brain is deliberately explainable rather than pretending to be a human-like general intelligence:

1. **Priority layer:** explicit stop, low battery, obstacle, person, then idle.
2. **Goal selector:** maps the selected state to a high-level goal such as `choose_clear_path`.
3. **Companion personality:** provides a small mood label (calm, careful, alert, friendly, curious).
4. **Episodic memory:** stores recent state changes and event notes in a bounded queue.
5. **Explanation:** returns a human-readable reason for each decision.

## Important limitations

- Sensor events are scripted for demonstration; there is no camera, object detector, microphone, or real sensor adapter.
- The model is a starter quadruped, not a validated dog robot design.
- The demo advances MuJoCo physics and holds a neutral actuator target; it does not implement a walking gait, balance controller, navigation planner, or autonomous obstacle avoidance.
- Memory is in RAM and is lost when the process exits.
- There is no language model wired into the control loop yet. A local LLM can later be added as a bounded, optional dialogue/planning component, never as a direct motor controller.
- This is a research prototype, not a real-world safety system. Do not connect it directly to physical motors.

## Next steps

1. Validate the MJCF model and add simulation smoke tests.
2. Add simulated range/contact sensors and derive observations from MuJoCo state rather than scripted events.
3. Implement and test a low-level controller and gait separately from the high-level brain.
4. Add persistent memory and optional local-model dialogue behind interfaces.
5. Add safety constraints and evaluate in simulation before any hardware work.
