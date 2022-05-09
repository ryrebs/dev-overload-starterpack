// Transform a chunk
const { Transform } = require("stream");

class ReplaceText extends Transform {
  constructor(char) {
    super();
    this.replaceChar = char;
  }
  _transform(chunk, encoding, callback) {
    const transformChunk = chunk
      .toString()
      .replace(/[a-z]|[A-Z][0-9]/g, this.replaceChar);
    this.push(transformChunk);
    callback();
  }

  // flush buffer
  _flush(callback) {
    this.push("More data passed");
    callback();
  }
}

var xStream = new ReplaceText("x");

process.stdin.pipe(xStream).pipe(process.stdout);
