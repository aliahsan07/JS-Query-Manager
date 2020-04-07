function StringBuffer() {
  this.array = [];
}

StringBuffer.prototype.append = function (x) {
  this.array.push(x);
};

var sb = new StringBuffer();
sb.append({});

var groundTruth = {
  "sb-9": 1
};
