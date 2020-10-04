/**
 *
 * @testcase_name with-3
 * @version 1.0
 * @description
 * @groundtruth_file with-3.ground
 */

var test = {
  a: {
    b: { c: 100 },
    d: { e: 200 },
  },
};

var t1 = test.a.b;
var t2 = test.a.d;

with (test.a) {
  b = { f: 101 };
}

t1 = test.a.b;
t2 = test.a.d;
