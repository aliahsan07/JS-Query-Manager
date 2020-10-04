/**
 *
 * @testcase_name prototype-1
 * @version 1.0
 * @description
 * @groundtruth_file prototype-1.ground
 */

var Person = {
  m: [5],
};
var y = Object.create(Person);
var z = y.m;

delete Person.m;
var z = y.m;
