/**
 *
 * @testcase_name eval-2
 * @version 1.0
 * @description
 * @groundtruth_file eval-2.ground
 */

function f() {
  return {
    evalWorks: true,
  };
}

var test = eval("f()");
