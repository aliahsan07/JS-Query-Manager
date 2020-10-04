/**
 *
 * @testcase_name flow-sensitivity-2
 * @version 1.0
 * @description explicit coercion
 * @groundtruth_file flow-sensitivity-2.ground
 */

var x = {};
var z = x.f;
x.f = {};
