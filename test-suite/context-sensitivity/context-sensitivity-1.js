/**
 *
 * @testcase_name context-sensitivity-1
 * @version 1.0
 * @description
 * @groundtruth_file context-sensitivity-1.ground
 */

function baseContextSensitivity(x) {
  return x;
}
var a = baseContextSensitivity({ A: "A" });
var d = baseContextSensitivity({ B: "B" });
