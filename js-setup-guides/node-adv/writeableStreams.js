const { createReadStream, createWriteStream } = require("fs");

const readStream = createReadStream("./sample.mp4");
const writeStream = createWriteStream("./copySample.mp4");

// copy file by chunck
readStream.on("data", chunk => writeStream.write(chunk));

readStream.on("error", error => console.log(error));

readStream.on("end", () => {
  writeStream.end();
});

writeStream.on("close", () => console.log("Done copying.."));
