import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ned_enu import ned_to_enu, FRAC_1_SQRT_2


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
]


@pytest.mark.parametrize(
    "name,start_rpy,end_rpy,q_in,expected",
    CASES,
)
def test_ned_to_enu(name, start_rpy, end_rpy, q_in, expected):
    result = ned_to_enu(q_in)
    np.testing.assert_allclose(result, expected)
