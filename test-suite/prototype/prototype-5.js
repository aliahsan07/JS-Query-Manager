function Student(name) {
  this.name = name;
  Student.prototype.count++;
}

Student.prototype.count = 0;

var x = new Student("Ali Ahsan");
var y = new Student("John Doe");

var groundTruth = {
  "x-8": 1,
  "y-9": 1
};
