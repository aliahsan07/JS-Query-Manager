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

var groundTruth = {
  "test1-15": 1,
  "test2-16": 1
};
