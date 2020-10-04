/**
 *
 * @testcase_name object-sensitivity-1
 * @version 1.0
 * @description
 * @groundtruth_file object-sensitivity-1.ground
 */

function X(num) {
  this.num = num;
}

function Y() {
  this.f = null;
  this.setF = function (x) {
    this.f = x;
  };
}

var x1 = new X("1");
var x2 = new X("2");
var y1 = new Y();
var y2 = new Y();
y1.setF(x1);
y2.setF(x2);

// y1.f should only point to x1
// y2.f should only point to x2
y1.f;
y2.f;
