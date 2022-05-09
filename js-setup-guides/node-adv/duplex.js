// can both be read and write stream

const { createReadStream, createWriteStream } = require("fs");
const { Duplex, PassThrough } = require("stream");
const readStream = createReadStream("./sample.mp4");
const writeStream = createWriteStream("./copySample.mp4");

// Custom duplex for delay reporting
class Throttle extends Duplex {
  constructor(ms) {
    super();
    this.delay = ms;
  }

  _write(chunk, encoding, callback) {
    this.push(chunk);
    setTimeout(callback, this.delay);
  }

  _read() {}

  _final() {
    this.push(null);
  }
}

// Duplex
const report = new PassThrough();
const throttle = new Throttle(100);

var total = 0;
report.on("data", chunk => {
  total += chunk.length;
  console.log("bytes: ", total);
});

// pipe to throttle  as both read and write for delaying
// pipe to report as writeable
// then pipe to writeStream as readable
readStream
  .pipe(throttle)
  .pipe(report)
  .pipe(writeStream);
