/**
 *
 * @testcase_name prototype-6
 * @version 1.0
 * @description
 * @groundtruth_file prototype-6.ground
 */

function funcObject() {
  this.a = {};
}

function myObject() {
  funcObject.call(this);
  this.b = {};
}

// myObject.prototype = Object.create(funcObject.prototype);

myObject.prototype = Object.create(funcObject.prototype);
var c = new myObject();
var d = new myObject();
var test1 = c.a;
var test2 = d.a;
