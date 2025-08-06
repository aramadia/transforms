import * as THREE from 'https://unpkg.com/three@0.179.1/build/three.module.js';

const FRAC_1_SQRT_2 = Math.sqrt(0.5);
const NED_TO_ENU = new THREE.Quaternion(FRAC_1_SQRT_2, FRAC_1_SQRT_2, 0, 0);
const ENU_TO_NED = NED_TO_ENU.clone().conjugate();

const inputTypeEl = document.getElementById('inputType');
const quaternionInputEl = document.getElementById('quaternionInput');
const axisInputEl = document.getElementById('axisInput');

const qw = document.getElementById('qw');
const qx = document.getElementById('qx');
const qy = document.getElementById('qy');
const qz = document.getElementById('qz');

const axEl = document.getElementById('ax');
const ayEl = document.getElementById('ay');
const azEl = document.getElementById('az');
const angleEl = document.getElementById('angle');

const inputFrameEl = document.getElementById('inputFrame');
const outputFrameEl = document.getElementById('outputFrame');

const outQuatEl = document.getElementById('outQuat');
const rotMatrixTable = document.getElementById('rotMatrix');
const outRPYEl = document.getElementById('outRPY');

function getInputQuaternion() {
  if (inputTypeEl.value === 'quaternion') {
    const w = parseFloat(qw.value) || 0;
    const x = parseFloat(qx.value) || 0;
    const y = parseFloat(qy.value) || 0;
    const z = parseFloat(qz.value) || 0;
    return new THREE.Quaternion(x, y, z, w).normalize();
  } else {
    const ax = parseFloat(axEl.value) || 0;
    const ay = parseFloat(ayEl.value) || 0;
    const az = parseFloat(azEl.value) || 0;
    const angle = parseFloat(angleEl.value) || 0;
    const axis = new THREE.Vector3(ax, ay, az);
    if (axis.lengthSq() === 0) {
      return new THREE.Quaternion();
    }
    axis.normalize();
    const q = new THREE.Quaternion();
    q.setFromAxisAngle(axis, THREE.MathUtils.degToRad(angle));
    return q;
  }
}

function convertFrame(q, fromF, toF) {
  if (fromF === toF) return q.clone();
  if (fromF === 'NED' && toF === 'ENU') {
    return NED_TO_ENU.clone().multiply(q);
  }
  if (fromF === 'ENU' && toF === 'NED') {
    return ENU_TO_NED.clone().multiply(q);
  }
  return q.clone();
}

function update() {
  const q = getInputQuaternion();
  const qOut = convertFrame(q, inputFrameEl.value, outputFrameEl.value).normalize();

  outQuatEl.textContent = `${qOut.w.toFixed(6)}, ${qOut.x.toFixed(6)}, ${qOut.y.toFixed(6)}, ${qOut.z.toFixed(6)}`;

  const m = new THREE.Matrix3().setFromMatrix4(new THREE.Matrix4().makeRotationFromQuaternion(qOut));
  const elems = m.elements;
  rotMatrixTable.innerHTML = '';
  for (let r = 0; r < 3; r++) {
    const row = document.createElement('tr');
    for (let c = 0; c < 3; c++) {
      const cell = document.createElement('td');
      const val = elems[c * 3 + r];
      cell.textContent = val.toFixed(6);
      row.appendChild(cell);
    }
    rotMatrixTable.appendChild(row);
  }

  const eul = new THREE.Euler().setFromQuaternion(qOut, 'XYZ');
  const roll = THREE.MathUtils.radToDeg(eul.x);
  const pitch = THREE.MathUtils.radToDeg(eul.y);
  const yaw = THREE.MathUtils.radToDeg(eul.z);
  outRPYEl.textContent = `${roll.toFixed(2)}, ${pitch.toFixed(2)}, ${yaw.toFixed(2)}`;
}

inputTypeEl.addEventListener('change', () => {
  if (inputTypeEl.value === 'quaternion') {
    quaternionInputEl.style.display = '';
    axisInputEl.style.display = 'none';
  } else {
    quaternionInputEl.style.display = 'none';
    axisInputEl.style.display = '';
  }
  update();
});

document.querySelectorAll('input, select').forEach(el => {
  el.addEventListener('input', update);
});

update();
