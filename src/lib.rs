pub type Quaternion = [f64; 4];

const FRAC_1_SQRT_2: f64 = std::f64::consts::FRAC_1_SQRT_2;
const NED_TO_ENU: Quaternion = [0.0, FRAC_1_SQRT_2, FRAC_1_SQRT_2, 0.0];

fn quat_mul(a: Quaternion, b: Quaternion) -> Quaternion {
    let [aw, ax, ay, az] = a;
    let [bw, bx, by, bz] = b;
    [
        aw * bw - ax * bx - ay * by - az * bz,
        aw * bx + ax * bw + ay * bz - az * by,
        aw * by - ax * bz + ay * bw + az * bx,
        aw * bz + ax * by - ay * bx + az * bw,
    ]
}

/// Convert a quaternion representing an orientation in the North-East-Down (NED)
/// frame into the equivalent quaternion in the East-North-Up (ENU) frame.
///
/// The quaternion is expected to be in `[w, x, y, z]` format and normalized.
/// The returned quaternion is also normalized.
pub fn ned_to_enu(q_ned: Quaternion) -> Quaternion {
    quat_mul(NED_TO_ENU, q_ned)
}

#[cfg(test)]
mod tests {
    use super::*;

    fn approx_eq(a: Quaternion, b: Quaternion) {
        let eps = 1e-10;
        for i in 0..4 {
            assert!((a[i] - b[i]).abs() < eps, "index {i} expected {} got {}", b[i], a[i]);
        }
    }

    #[test]
    fn identity_orientation() {
        let q = [1.0, 0.0, 0.0, 0.0];
        let expected = [0.0, FRAC_1_SQRT_2, FRAC_1_SQRT_2, 0.0];
        approx_eq(ned_to_enu(q), expected);
    }

    #[test]
    fn yaw_90_becomes_roll_180() {
        let a = FRAC_1_SQRT_2;
        let q_yaw_90 = [a, 0.0, 0.0, a];
        let expected = [0.0, 1.0, 0.0, 0.0];
        approx_eq(ned_to_enu(q_yaw_90), expected);
    }

    #[test]
    fn yaw_180_results() {
        let q_yaw_180 = [0.0, 0.0, 0.0, 1.0];
        let a = FRAC_1_SQRT_2;
        let expected = [0.0, a, -a, 0.0];
        approx_eq(ned_to_enu(q_yaw_180), expected);
    }
}
