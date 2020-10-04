/**
 *
 * @testcase_name property-name-3
 * @version 1.0
 * @description
 * @groundtruth_file property-name-3.ground
 */

var t = {
  a: [1, 2, 3],
  b: { c: 3 },
};

var c = {};

for (var prop in t) {
  c[prop] = t[prop];
}

var t1 = c.a;
