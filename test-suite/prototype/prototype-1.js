function StringBuffer() {
  this.array = [];
}

StringBuffer.prototype.append = function (x) {
  this.array.push(x);
};

StringBuffer.prototype.toString = function () {
  return this.array.join("");
};
var sb = new StringBuffer();
sb.append("foo");
sb.append("bar");
