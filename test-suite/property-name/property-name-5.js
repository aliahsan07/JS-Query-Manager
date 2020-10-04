/**
 *
 * @testcase_name property-name-4
 * @version 1.0
 * @description
 * @groundtruth_file property-name-4.ground
 */

var x;

var y = {
  a: [1, 2],
  b: [3, 4, 5],
};

for (var c in y) {
  x = y[c];
}

var test = x;
