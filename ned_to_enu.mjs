import { Quaternion } from 'three';

const FRAC_1_SQRT_2 = Math.sqrt(0.5);
const NED_TO_ENU = new Quaternion(FRAC_1_SQRT_2, FRAC_1_SQRT_2, 0.0, 0.0);

function parseArgs() {
  const args = process.argv.slice(2);
  const impl = args.shift();
  if (impl !== 'threejs') {
    console.error(`unknown implementation: ${impl}`);
    process.exit(1);
  }
  if (args.length !== 4) {
    console.error('usage: node ned_to_enu.mjs threejs <w> <x> <y> <z>');
    process.exit(1);
  }
  const nums = args.map((v, i) => {
    const n = Number(v);
    if (Number.isNaN(n)) {
      console.error(`invalid float: ${v}`);
      process.exit(1);
    }
    return n;
  });
  return nums; // [w,x,y,z]
}

function nedToEnu(qNed) {
  const [w, x, y, z] = qNed;
  const q = new Quaternion(x, y, z, w);
  const result = NED_TO_ENU.clone().multiply(q);
  return [result.w, result.x, result.y, result.z];
}

function main() {
  const qNed = parseArgs();
  const result = nedToEnu(qNed);
  console.log(result.join(' '));
}

main();
