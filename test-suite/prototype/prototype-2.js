/**
 *
 * @testcase_name prototype-2
 * @version 1.0
 * @description
 * @groundtruth_file prototype-2.ground
 */

var Person = {
  m: [5],
};
var y = Object.create(Person);
var z = y.m;
y.m = [10];
