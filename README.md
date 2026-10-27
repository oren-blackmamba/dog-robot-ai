# Dog Robot AI

**An open-source foundation for an AI-powered robotic dog companion.**

Dog Robot AI is a software-first project exploring how a quadruped robot could perceive its environment, choose safe behaviors, interact with people, and eventually move through a physics-based simulation.

The initial version contains a dependency-free behavior controller and automated tests. It does **not** claim to control physical hardware yet.

## Project goals

- **Behavior:** make clear, testable decisions from simple sensor observations.
- **Perception:** later integrate cameras and computer-vision models.
- **Simulation:** add a quadruped model and physics-based experiments using MuJoCo.
- **Companion interaction:** explore human-aware behaviors and configurable interaction modes.
- **Local-first AI:** keep future inference modular so local models can be used where practical.
- **Safety:** make stop, obstacle, and low-battery behavior explicit and testable.

## Current status

The initial behavior layer is a prototype for software development and testing only. It is not a certified robotics controller and must not be connected directly to motors or used as a real-world safety system.

## Quick start

Requires Python 3.10 or newer. The core controller uses only the Python standard library.

**Windows PowerShell** (from the repository root):

```powershell
$env:PYTHONPATH = "src"
python -m dog_robot_ai
python -m unittest discover -s tests -v
```

**macOS / Linux**:

```bash
PYTHONPATH=src python -m dog_robot_ai
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Repository layout

```text
src/dog_robot_ai/   Core behavior logic and demo entry point
tests/              Automated unit tests
docs/               Architecture notes and development roadmap
```

## Behavior priority

The first controller applies this priority order:

1. Explicit stop command
2. Critically low battery → request return to charging
3. Obstacle detected → request obstacle avoidance
4. Person detected → companion interaction state
5. Otherwise → idle state

These are high-level software states, not walking trajectories or motor commands.

## Roadmap

- [x] Create a minimal Python package structure
- [x] Add a deterministic behavior controller
- [x] Add automated unit tests
- [x] Document architecture and limitations
- [ ] Add optional MuJoCo simulation integration
- [ ] Define sensor interfaces and structured event logging
- [ ] Add a perception adapter with mocked inputs for tests
- [ ] Evaluate local language/vision models behind replaceable interfaces
- [ ] Add hardware integration only after simulation and safety reviews

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Small pull requests with tests and clear explanations are welcome.

## License

This project is released under the [MIT License](LICENSE).
