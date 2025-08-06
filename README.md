# Transforms

This repository provides quaternion transforms between North-East-Down (NED) and East-North-Up (ENU) reference frames.

## JavaScript (Three.js)

A JavaScript implementation powered by the `three` package is provided via `ned_to_enu.mjs`. Install the dependency with `npm install`.

```
node ned_to_enu.mjs threejs <w> <x> <y> <z>
```

- `<w> <x> <y> <z>` – components of the quaternion in the NED frame.
- Prints the corresponding quaternion in the ENU frame to stdout.

The interface matches the Rust binary where the first argument selects the implementation (`threejs` here) followed by the quaternion components.
