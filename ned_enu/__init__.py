import numpy as np

# Quaternion representing transformation from NED to ENU frame
# Format: [w, x, y, z]
FRAC_1_SQRT_2 = np.sqrt(0.5)
NED_TO_ENU = np.array([0.0, FRAC_1_SQRT_2, FRAC_1_SQRT_2, 0.0])


def quat_mul(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Multiply two quaternions given in [w, x, y, z] format."""
    aw, ax, ay, az = a
    bw, bx, by, bz = b
    return np.array([
        aw * bw - ax * bx - ay * by - az * bz,
        aw * bx + ax * bw + ay * bz - az * by,
        aw * by - ax * bz + ay * bw + az * bx,
        aw * bz + ax * by - ay * bx + az * bw,
    ])


def ned_to_enu(q_ned: np.ndarray) -> np.ndarray:
    """Convert a quaternion from NED to ENU reference frame.

    Parameters
    ----------
    q_ned : array_like
        Quaternion in [w, x, y, z] format representing an orientation in the
        North-East-Down frame.

    Returns
    -------
    np.ndarray
        Quaternion representing the same orientation in the East-North-Up frame.
    """
    q_ned = np.asarray(q_ned, dtype=float)
    return quat_mul(NED_TO_ENU, q_ned)
