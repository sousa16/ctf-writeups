const keys = [
  'copy_char', 'value', '207aLjBod', '1301420SaUSqf', '233ZRpipt', '2224QffgXU',
  'check_flag', '408533hsoVYx', 'instance', '278338GVFUrH', 'Correct!',
  '549933ZVjkwI', 'innerHTML', 'charCodeAt', './aD8SvhyVkb', 'result',
  '977AzKzwq', 'Incorrect!', 'exports', 'length', 'getElementById',
  '1jIrMBu', 'input', '615361geljRK'
];

function decode(idx) {
  return keys[idx - 0xc3];
}

// Array shuffle for obfuscation (irrelevant for logic)
(function(arr, target) {
  while (true) {
    try {
      const val = -parseInt(decode(0xc8)) * -parseInt(decode(0xc9))
        + -parseInt(decode(0xcd))
        + parseInt(decode(0xcf))
        + parseInt(decode(0xc3))
        + -parseInt(decode(0xc6)) * parseInt(decode(0xd4))
        + parseInt(decode(0xcb))
        + -parseInt(decode(0xd9)) * parseInt(decode(0xc7));
      if (val === target) break;
      else arr.push(arr.shift());
    } catch (e) {
      arr.push(arr.shift());
    }
  }
})(keys, 0x4bb06);

let exports;
(async () => {
  let wasm = await fetch(decode(0xd2));
  let instance = await WebAssembly.instantiate(await wasm.arrayBuffer());
  exports = instance[decode(0xcc)][decode(0xd6)];
})();

function onButtonPress() {
  let input = document.getElementById(decode(0xda)).value;
  for (let i = 0; i < input.length; i++) {
    exports.copy_char(input.charCodeAt(i), i);
  }
  exports.copy_char(0, input.length);
  if (exports.check_flag() == 1) {
    document.getElementById(decode(0xd3)).innerHTML = decode(0xce); // "Correct!"
  } else {
    document.getElementById(decode(0xd3)).innerHTML = decode(0xd5); // "Incorrect!"
  }
}