# Dog Robot AI

**An open-source foundation for an AI-powered robotic dog companion.**

Dog Robot AI is a software-first project exploring how a quadruped robot could perceive its environment, choose safe behaviors, interact with people, and eventually move through a physics-based simulation.

The project now includes a deterministic behavior controller, a stateful companion brain with bounded episodic memory, and an optional MuJoCo simulation bridge with a starter four-legged model.

## Current status

This is a simulation-oriented software prototype. The brain can choose high-level states and goals, label a simple mood, explain its decision, and remember recent events while running. The MuJoCo demo currently uses scripted example events and a neutral actuator target.

It does **not** yet have camera-based perception, a walking gait, balance or navigation control, a connected language model, persistent memory, or physical robot integration. Do not connect it directly to real motors.

## Quick start

Requires Python 3.10 or newer.

**Core brain and tests — no third-party runtime dependency:**

Windows PowerShell:
```powershell
$env:PYTHONPATH = "src"
python -m dog_robot_ai
python -m unittest discover -s tests -v
```

macOS / Linux:
```bash
PYTHONPATH=src python -m dog_robot_ai
PYTHONPATH=src python -m unittest discover -s tests -v
```

**Optional MuJoCo simulation:**

Install the package with the simulation extra, then launch the visual demo:
```bash
python -m pip install -e ".[simulation]"
PYTHONPATH=src python -m dog_robot_ai.mujoco_sim
```

On Windows PowerShell, set `$env:PYTHONPATH = "src"` before running the module. A desktop graphics session is needed for the viewer.

See [docs/MUJOCO_BRAIN.md](docs/MUJOCO_BRAIN.md) for details and limitations.

## How the brain works

1. **Priority layer:** stop command, low battery, obstacle, person, then idle.
2. **Goal selection:** chooses a high-level goal such as `stop_and_wait`, `find_charging_station`, or `choose_clear_path`.
3. **Companion personality:** adds a simple mood label such as calm, careful, alert, friendly, or curious.
4. **Memory:** stores a bounded history of recent state changes and events in RAM.
5. **Explanation:** provides a readable reason for the current decision.

This is an explainable rule-based prototype, not general intelligence or a trained AI model.

## Project goals

- **Behavior:** make clear, testable decisions from sensor observations.
- **Perception:** later integrate cameras and computer-vision models.
- **Simulation:** develop and test a quadruped model using MuJoCo.
- **Companion interaction:** explore human-aware behaviors and configurable interaction modes.
- **Local-first AI:** keep future inference modular so local models can be used where practical.
- **Safety:** make stop, obstacle, and low-battery behavior explicit and testable.

## Repository layout

```text
src/dog_robot_ai/   Behavior controller, brain, memory, and simulation bridge
simulation/         Starter MuJoCo quadruped model
tests/              Automated unit tests
docs/               Architecture and simulation notes
```

## Roadmap

- [x] Minimal Python package and deterministic behavior controller
- [x] Automated unit tests for behavior priorities
- [x] Stateful brain with goal selection, mood labels, explanations, and bounded memory
- [x] Starter quadruped MJCF model and optional MuJoCo bridge
- [ ] Validate the MuJoCo model in an installed simulation environment
- [ ] Derive observations from simulated sensors rather than scripted events
- [ ] Add perception adapters with mocked inputs for tests
- [ ] Add a gait, balance controller, and navigation planner as separate modules
- [ ] Add optional local-model dialogue/planning behind controlled interfaces
- [ ] Add hardware integration only after simulation and safety reviews

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Small pull requests with tests and clear explanations are welcome.

## License

This project is released under the [MIT License](LICENSE).
