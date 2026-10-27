# Contributing

Thanks for your interest in Dog Robot AI.

## Principles

- Keep modules small and focused.
- Prefer deterministic behavior and explicit interfaces.
- Add tests for new behavior and bug fixes.
- Clearly distinguish simulated, mocked, and hardware-tested functionality.
- Do not add credentials, personal data, or unlicensed third-party assets.
- Do not describe prototype behavior as production-ready or safety-certified.

## Development setup

Python 3.10 or newer is required. The core package currently has no runtime dependencies.

From the repository root:

```bash
pip install -e .
python -m unittest discover -s tests -v
python -m dog_robot_ai
```

If you prefer not to install the package, use the `PYTHONPATH=src` instructions in the README.

## Pull requests

1. Describe the problem and the proposed change.
2. Keep each pull request focused.
3. Add or update tests where relevant.
4. Include the exact commands used to test the change.
5. State whether results come from unit tests, simulation, or physical hardware.

For significant architecture changes, open an issue or discussion first.
