use std::env;

use transforms::{ned_to_enu_manual, ned_to_enu_nalgebra};

fn main() {
    let mut args = env::args().skip(1);
    let impl_type = args.next().expect("expected implementation type");

    let mut q = [0f64; 4];
    for i in 0..4 {
        let arg = args
            .next()
            .unwrap_or_else(|| panic!("missing quaternion component {i}"));
        q[i] = arg.parse().expect("invalid float");
    }

    let result = match impl_type.as_str() {
        "manual" => ned_to_enu_manual(q),
        "nalgebra" => ned_to_enu_nalgebra(q),
        other => {
            eprintln!("unknown implementation: {other}");
            std::process::exit(1);
        }
    };

    println!("{} {} {} {}", result[0], result[1], result[2], result[3]);
}
