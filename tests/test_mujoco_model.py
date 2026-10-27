"""Smoke tests for the optional MuJoCo model and physics loop."""
from pathlib import Path
import unittest

try:
    import mujoco
except ImportError:  # Core-only installs do not require MuJoCo.
    mujoco = None


MODEL_PATH = Path(__file__).resolve().parents[1] / "simulation" / "dog_quadruped.xml"


@unittest.skipIf(mujoco is None, "MuJoCo simulation extra is not installed")
class MuJoCoModelTests(unittest.TestCase):
    def test_model_loads_with_expected_joints_and_actuators(self):
        model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))
        self.assertEqual(model.njnt, 9)  # free root + 8 leg joints
        self.assertEqual(model.nu, 8)
        self.assertGreater(model.nbody, 1)

    def test_physics_steps_without_non_finite_state(self):
        model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))
        data = mujoco.MjData(model)
        for _ in range(500):
            mujoco.mj_step(model, data)
        self.assertTrue(all(map(__import__("math").isfinite, data.qpos)))
        self.assertTrue(all(map(__import__("math").isfinite, data.qvel)))
        self.assertGreater(data.time, 0.0)


if __name__ == "__main__":
    unittest.main()
