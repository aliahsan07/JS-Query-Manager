var foo1 = function () {
  this.baz1 = 42;
};
var foo2 = function () {};

foo2.prototype = new foo1();

var xxx = new foo2();
var y1 = xxx.baz1;

new foo1();
