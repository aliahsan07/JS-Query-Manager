/**
 *
 * @testcase_name with-2
 * @version 1.0
 * @description
 * @groundtruth_file with-2.ground
 */

function foo(obj) {
  with (obj) {
    a = { a: 2 };
  }
}

var o1 = {
  a: { a: 3 },
};

var o2 = {
  b: { b: 3 },
};

foo(o1);

foo(o2);
var t1 = o1.a;
var t2 = o2.a; // undefined
var t3 = a; // leaked global
