/**
 *
 * @testcase_name context-sensitivity-2
 * @version 1.0
 * @description
 * @groundtruth_file context-sensitivity-2.ground
 */

function testCxtSen(property, obj) {
  return obj[property];
}

var obj = {
  first: [1, 2, 3],
  second: new String("any string"),
  third: {},
};

for (var prop in obj) {
  obj[prop] = testCxtSen(prop, obj);
}

var secondObj = obj["second"];
