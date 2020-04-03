function Vector(x, y) {
  this.x = x || 0;
  this.y = y || 0;
}
Vector.prototype.add = function (v, y) {
  if (v instanceof Vector) {
    this.x += v.x;
    this.y += v.y;
  } else {
    this.x += v || 0;
    this.y += y || 0;
  }
};
var a = new Vector(); // x: 0, y: 0
a.add(new Vector(1, 2)); // x: 1, y: 2
a.add(10, 30);
