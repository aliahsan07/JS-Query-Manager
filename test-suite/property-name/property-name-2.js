/**
 *
 * @testcase_name property-name-1
 * @version 1.0
 * @description
 * @groundtruth_file property-name-1.ground
 */

var src = {
  alpha: 1,
  beta: "testing",
  gamma: new Boolean(true),
};

var dest = {};
for (var prop in src) {
  dest[prop] = src[prop];
}
