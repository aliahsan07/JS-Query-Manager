/**
 *
 * @testcase_name prototype-5
 * @version 1.0
 * @description
 * @groundtruth_file prototype-5.ground
 */

var a = {
  a: {},
};

var b = Object.create(a);
b.a = [];

var c = b.a;

delete b.a;
c = b.a;
delete a.a;
c = b.a;
