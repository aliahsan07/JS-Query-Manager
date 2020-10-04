/**
 *
 * @testcase_name closure-2
 * @version 1.0
 * @description
 * @groundtruth_file closure-2.ground
 */

function init() {
  var name = Math.random() > 0.5 ? [] : {};
  function displayName() {
    var n = name;
  }
  displayName();
}
init();
