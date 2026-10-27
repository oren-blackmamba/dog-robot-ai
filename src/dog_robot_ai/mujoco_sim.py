"""Optional MuJoCo bridge for the Dog Robot AI prototype.

Install with: pip install -e ".[simulation]"
Run with: python -m dog_robot_ai.mujoco_sim
"""
from pathlib import Path

from .behavior import SensorSnapshot
from .brain import DogBrain


MODEL_PATH = Path(__file__).resolve().parents[2] / "simulation" / "dog_quadruped.xml"


def run_demo(steps: int = 1500, show_viewer: bool = True) -> None:
    """Run a simple physics scene and feed simulated observations to DogBrain."""
    try:
        import mujoco
    except ImportError as exc:
        raise SystemExit(
            'MuJoCo is optional. Install it with: pip install -e ".[simulation]"'
        ) from exc

    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"MuJoCo model not found: {MODEL_PATH}")

    model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))
    data = mujoco.MjData(model)
    brain = DogBrain()
    viewer = None

    if show_viewer:
        try:
            import mujoco.viewer
            viewer = mujoco.viewer.launch_passive(model, data)
        except Exception as exc:
            raise SystemExit(
                "Could not open the MuJoCo viewer. Try running in a desktop session "
                "or call run_demo(show_viewer=False). Details: " + str(exc)
            ) from exc

    print("Dog AI + MuJoCo demo started. Observations are scripted, not from real sensors.")
    try:
        for step in range(steps):
            # Scripted test events demonstrate the brain; they are not computer vision.
            person = 250 <= step < 650
            obstacle = 700 <= step < 900
            battery = 8.0 if step >= 1200 else 78.0
            command = "stop" if 1000 <= step < 1050 else "idle"
            decision = brain.think(SensorSnapshot(
                battery_percent=battery,
                obstacle_detected=obstacle,
                person_detected=person,
                command=command,
            ))

            # Keep a stable neutral posture. This demo does not implement a gait.
            mujoco.mj_step(model, data)
            if step % 100 == 0:
                print(
                    f"step={step:04d} state={decision.state.value:<16} "
                    f"goal={decision.goal:<24} mood={decision.mood:<8} "
                    f"memories={decision.memory_count}"
                )
            if viewer is not None:
                if not viewer.is_running():
                    break
                viewer.sync()
    finally:
        if viewer is not None:
            viewer.close()
    print("Demo finished. No real robot or motors were controlled.")


if __name__ == "__main__":
    run_demo()
