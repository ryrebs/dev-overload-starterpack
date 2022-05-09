const fs = require("fs");

const readStream = fs.createReadStream("./sample.mp4");

// flowing
readStream.on("data", chunk => console.log(chunk, "size: ", chunk.length));

readStream.on("end", () => console.log("No chunk left"));

readStream.on("error", error => console.log(error));

// convert to non flowing
// ask data per stdin
readStream.pause();
process.stdin.on("data", chunk => {
  // get input from stdin
  // and display the text
  var text = chunk.toString().trim();
  console.log("echo: ", text);

  if (chunk.toString().trim() === "finish") {
    readStream.resume();
  }
  // read one chunk per stdin
  readStream.read();
});
