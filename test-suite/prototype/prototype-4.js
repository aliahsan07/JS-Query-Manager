function Student(name) {
  this.name = name;
  Student.prototype.count++;
}

Student.prototype.count = { x: 0 };

var x = new Student("Ali Ahsan");
var y = new Student("John Doe");

// check if there is a count
// z = x.count (make count an object instead of primitive)
// student.prototype.f when you intialize it
// reassign that count to some other object, whats the size of x.f
// delete a field (delete a whole prototype), should not be a points to set

var groundTruth = {
  "x-8": 1,
  "y-9": 1
};
