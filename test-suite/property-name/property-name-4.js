/**
 *
 * @testcase_name property-name-4
 * @version 1.0
 * @description
 * @groundtruth_file property-name-4.ground
 */

var t = {
  [24]: [1, 2, 3],
  [1]: { c: 3 },
};

var c = {};

for (var prop in t) {
  c[prop] = t[prop];
}

var t1 = c[prop];
var t2 = prop;
