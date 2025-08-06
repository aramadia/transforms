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

/// Hand-written quaternion multiplication implementation of the transform.
pub fn ned_to_enu_manual(q_ned: Quaternion) -> Quaternion {
    quat_mul(NED_TO_ENU, q_ned)
}

/// Implementation of the transform using the `nalgebra` crate.
pub fn ned_to_enu_nalgebra(q_ned: Quaternion) -> Quaternion {
    use nalgebra::Quaternion as NQuaternion;

    let rot = NQuaternion::new(NED_TO_ENU[0], NED_TO_ENU[1], NED_TO_ENU[2], NED_TO_ENU[3]);
    let q = NQuaternion::new(q_ned[0], q_ned[1], q_ned[2], q_ned[3]);
    let r = rot * q;
    [r.w, r.i, r.j, r.k]
}

/// Default transform exposed for consumers. Currently uses the manual version.
pub fn ned_to_enu(q_ned: Quaternion) -> Quaternion {
    ned_to_enu_manual(q_ned)
}

#[cfg(test)]
mod tests {
    use super::*;

    type Transform = fn(Quaternion) -> Quaternion;

    fn approx_eq(a: Quaternion, b: Quaternion) {
        let eps = 1e-10;
        for i in 0..4 {
            assert!((a[i] - b[i]).abs() < eps, "index {i} expected {} got {}", b[i], a[i]);
        }
    }

    #[derive(Clone, Copy)]
    struct Case {
        name: &'static str,
        start_rpy_deg: (f64, f64, f64),
        end_rpy_deg: (f64, f64, f64),
        input: Quaternion,
        expected: Quaternion,
    }

    const A: f64 = FRAC_1_SQRT_2;

    const CASES: &[Case] = &[
        Case {
            name: "identity orientation",
            start_rpy_deg: (0.0, 0.0, 0.0),
            end_rpy_deg: (180.0, 0.0, 90.0),
            input: [1.0, 0.0, 0.0, 0.0],
            expected: [0.0, A, A, 0.0],
        },
        Case {
            name: "yaw 90° becomes roll 180°",
            start_rpy_deg: (0.0, 0.0, 90.0),
            end_rpy_deg: (180.0, 0.0, 0.0),
            input: [A, 0.0, 0.0, A],
            expected: [0.0, 1.0, 0.0, 0.0],
        },
        Case {
            name: "yaw 180° becomes roll 180° with yaw -90°",
            start_rpy_deg: (0.0, 0.0, 180.0),
            end_rpy_deg: (180.0, 0.0, -90.0),
            input: [0.0, 0.0, 0.0, 1.0],
            expected: [0.0, A, -A, 0.0],
        },
    ];

    const IMPLS: &[(&str, Transform)] = &[
        ("manual", ned_to_enu_manual as Transform),
        ("nalgebra", ned_to_enu_nalgebra as Transform),
    ];

    #[test]
    fn implementations_match_expected() {
        for case in CASES {
            for (impl_name, f) in IMPLS {
                let result = f(case.input);
                approx_eq(result, case.expected);
                // print orientation context for easier debugging if the test fails
                println!(
                    "{impl_name} | {}: start rpy {:?} -> end rpy {:?}",
                    case.name, case.start_rpy_deg, case.end_rpy_deg
                );
            }
        }
    }
}
