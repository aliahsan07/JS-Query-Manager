/**
 *
 * @testcase_name property-name-1
 * @version 1.0
 * @description
 * @groundtruth_file property-name-1.ground
 */

var foo = {};
var obj = { a: {}, b: {} };

for (var name in obj) {
  var name_obj = { name: name };

  foo[name_obj.name] = obj[name_obj.name];
}
