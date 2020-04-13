function X(num) {
  this.num = num;
}

function Y() {
  this.f = null;
}

Y.prototype.setF = function (x) {
  this.f = x;
};

var x1 = new X(1);
var x2 = new X(2);
var y1 = new Y();
var y2 = new Y();

y1.setF(x1);
y2.setF(x2);

y1.f;
y2.f;

var groundTruth = {
  "f-21": 1,
  "f-22": 1
};
