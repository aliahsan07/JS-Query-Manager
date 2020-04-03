// MDN Example:
var f = function () {
  this.a = 1;
  this.b = 2;
};
var o = new f();

f.prototype.b = 3;
f.prototype.c = 4;
