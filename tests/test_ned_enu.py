import os
import sys
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ned_enu import ned_to_enu, FRAC_1_SQRT_2


def test_identity_orientation():
    q = np.array([1.0, 0.0, 0.0, 0.0])
    expected = np.array([0.0, FRAC_1_SQRT_2, FRAC_1_SQRT_2, 0.0])
    np.testing.assert_allclose(ned_to_enu(q), expected)


def test_yaw_90_becomes_roll_180():
    a = FRAC_1_SQRT_2
    q_yaw_90 = np.array([a, 0.0, 0.0, a])
    expected = np.array([0.0, 1.0, 0.0, 0.0])
    np.testing.assert_allclose(ned_to_enu(q_yaw_90), expected)


def test_yaw_180_results():
    q_yaw_180 = np.array([0.0, 0.0, 0.0, 1.0])
    a = FRAC_1_SQRT_2
    expected = np.array([0.0, a, -a, 0.0])
    np.testing.assert_allclose(ned_to_enu(q_yaw_180), expected)
