// backpressure handles stream if it can't write anymore to host
const { createReadStream, createWriteStream } = require("fs");

const readStream = createReadStream("./sample.mp4");
const writeStream = createWriteStream("./copySample.mp4", {
  // set large host to set large buffer/memory and lessen backpressure
  highWaterMark: 162820
});

// copy file by chunk
readStream.on("data", chunk => {
  // capture result
  // true means can still write
  // false otherwise
  const result = writeStream.write(chunk);
  if (!result) {
    // Backpressure is happening
    console.log("Backpressure");
  }
});

readStream.on("error", error => console.log(error));

readStream.on("end", () => {
  writeStream.end();
});

// listen to streams when it is drained
writeStream.on("drain", () => {
  console.log("Draining");
  readStream.resume();
});

writeStream.on("close", () => console.log("Done copying.."));
