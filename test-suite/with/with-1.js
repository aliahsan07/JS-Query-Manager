/**
 *
 * @testcase_name with-1
 * @version 1.0
 * @description
 * @groundtruth_file with-1.ground
 */

function foo(obj) {
  var prefix = "Hello ";
  with (obj) {
    console.log(prefix + msg);
  }
}

o1 = { msg: "World" };
foo(o1); // ’Hello World’
