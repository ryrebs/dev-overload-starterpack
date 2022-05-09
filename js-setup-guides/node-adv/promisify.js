// callback pattern
const delay = (seconds, cb) => {
  // Convention for callback: pass error as first argument
  if (seconds > 3) {
    cb(new Error("Too much time"));
  } else {
    setTimeout(() => {
      cb(null, `${seconds} delay is over`);
    });
  }
};

delay(4, (error, message) => {
  if (error) {
    console.log(error.message);
  } else {
    console.log(message);
  }
});

// converting to promise
const { promisify } = require("util");
const promiseDelay = promisify(delay);

promiseDelay(2)
  .then(console.log)
  .catch(error => console.log(`error: ${error.message}`));

// using callback with fs
const fs = require("fs");
var { promisfy } = require("util");

// writeFile is using callback pattern so
// convert it
var writeFile = promisify(fs.writeFile);

writeFile("sample.txt", "This is a sample text")
  .then(() => console.log("Succesfully created textfile"))
  .catch(err => console.error(err));
