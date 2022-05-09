// Any read stream can pipe to write stream
const { createWriteStream } = require("fs");

const writeStream = createWriteStream("./file.txt");

// handles backpressure automatically
// process is a readable stream
process.stdin.pipe(writeStream);
