/**
 *
 * @testcase_name eval-2
 * @version 1.0
 * @description
 * @groundtruth_file eval-2.ground
 */

function f() {
  const a =  {
    evalWorks: true,
  };
  return a;
}

var test = eval("f()");
