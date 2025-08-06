import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest
from scipy.spatial.transform import Rotation as R

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ned_enu import ned_to_enu, FRAC_1_SQRT_2


def rpy_to_quat(rpy: tuple[float, float, float]) -> np.ndarray:
    """Convert roll, pitch, yaw (degrees) to a quaternion [w, x, y, z]."""
    # SciPy returns quaternions in [x, y, z, w] order; rotate to [w, x, y, z]
    return np.roll(R.from_euler("xyz", rpy, degrees=True).as_quat(), 1)


def quat_to_rpy(q: np.ndarray) -> np.ndarray:
    """Convert quaternion [w, x, y, z] to roll, pitch, yaw (degrees)."""
    # Rotate to SciPy's [x, y, z, w] order before conversion
    return R.from_quat(np.roll(q, -1)).as_euler("xyz", degrees=True)


def assert_quat_allclose(a: np.ndarray, b: np.ndarray) -> None:
    """Assert two quaternions are equal up to sign."""
    if np.allclose(a, b) or np.allclose(a, -b):
        return
    np.testing.assert_allclose(a, b)


A = FRAC_1_SQRT_2

CASES = [
    (
        "identity orientation",
        (0.0, 0.0, 0.0),
        (180.0, 0.0, 90.0),
        np.array([1.0, 0.0, 0.0, 0.0]),
        np.array([0.0, A, A, 0.0]),
    ),
    (
        "yaw 90° becomes roll 180°",
        (0.0, 0.0, 90.0),
        (180.0, 0.0, 0.0),
        np.array([A, 0.0, 0.0, A]),
        np.array([0.0, 1.0, 0.0, 0.0]),
    ),
    (
        "yaw 180° becomes roll 180° with yaw -90°",
        (0.0, 0.0, 180.0),
        (180.0, 0.0, -90.0),
        np.array([0.0, 0.0, 0.0, 1.0]),
        np.array([0.0, A, -A, 0.0]),
    ),
    (
        "pitch 10° nose up",
        (0.0, 10.0, 0.0),
        (180.0, -10.0, 90.0),
        np.array([0.9961947, 0.0, 0.08715574, 0.0]),
        np.array([-0.06162842, 0.70441603, 0.70441603, 0.06162842]),
    ),
    (
        "pitch -10° nose down",
        (0.0, -10.0, 0.0),
        (180.0, 10.0, 90.0),
        np.array([0.9961947, 0.0, -0.08715574, 0.0]),
        np.array([0.06162842, 0.70441603, 0.70441603, -0.06162842]),
    ),
    (
        "roll 45° bank left",
        (45.0, 0.0, 0.0),
        (-135.0, 0.0, 90.0),
        np.array([0.92387953, 0.38268343, 0.0, 0.0]),
        np.array([-0.27059805, 0.65328148, 0.65328148, -0.27059805]),
    ),
]

ROOT = Path(__file__).resolve().parent.parent
IMPLS = ["manual", "nalgebra", "threejs"]


def run_impl(impl_name: str, q: np.ndarray) -> np.ndarray:
    if impl_name in {"manual", "nalgebra"}:
        cmd = ["cargo", "run", "--quiet", "--", impl_name] + [str(x) for x in q]
    elif impl_name == "threejs":
        node_modules = ROOT / "node_modules" / "three"
        if not node_modules.exists():
            subprocess.run(["npm", "install", "--silent"], check=True, cwd=ROOT)
        cmd = ["node", "ned_to_enu.mjs", impl_name] + [str(x) for x in q]
    else:
        raise ValueError(f"unknown implementation {impl_name}")

    completed = subprocess.run(
        cmd, capture_output=True, check=True, text=True, cwd=ROOT
    )
    return np.fromstring(completed.stdout.strip(), sep=" ")


@pytest.mark.parametrize(
    "name,start_rpy,end_rpy,q_in,expected",
    CASES,
)
def test_ned_to_enu(name, start_rpy, end_rpy, q_in, expected):
    # Verify the provided quaternions encode the stated roll, pitch, yaw values
    np.testing.assert_allclose(quat_to_rpy(q_in), start_rpy)
    np.testing.assert_allclose(quat_to_rpy(expected), end_rpy)
    assert_quat_allclose(rpy_to_quat(start_rpy), q_in)
    assert_quat_allclose(rpy_to_quat(end_rpy), expected)

    # Run the Python implementation and ensure it matches the expected quaternion
    expected_python = ned_to_enu(q_in)
    np.testing.assert_allclose(expected_python, expected)

    for impl_name in IMPLS:
        result = run_impl(impl_name, q_in)
        np.testing.assert_allclose(result, expected_python)
