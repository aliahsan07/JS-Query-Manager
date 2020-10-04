/**
 *
 * @testcase_name closure-3
 * @version 1.0
 * @description
 * @groundtruth_file closure-3.ground
 */

var arr = [];
var i;

for (i = 0; i < 10; i++) {
  try {
    throw true;
  } catch (x) {
    arr[i] = {
      setX: function (v) {
        x = v;
      },
      getX: function () {
        return x;
      },
    };
  }
}

arr[0].setX(10);
arr[1].setX("ABC");
