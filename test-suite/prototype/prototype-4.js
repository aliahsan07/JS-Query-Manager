function Student(name) {
  this.name = name;
  Student.prototype.count.x++;
}

Student.prototype.count = { x: 0 };

var x = new Student("Ali Ahsan");
var y = new Student("John Doe");

// check if there is a count
var xCount = x.count;
var yCount = y.count;

// student.prototype.f when you intialize it
// reassign that count to some other object, whats the size of x.f
// delete a field (delete a whole prototype), should not be a points to set

var groundTruth = {
  "xCount-12": 1,
  "yCount-13": 1
};
