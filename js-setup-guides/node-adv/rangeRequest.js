// Handling range request to streams

const { createServer } = require("http");
const { stat, createReadStream } = require("fs");
const { promisify } = require("util");
const fileName = "./sample.mp4";
const fileInfo = promisify(stat);

createServer(async (req, res) => {
  const { size } = await fileInfo(fileName);
  const range = req.headers.range;
  // check if there is range request
  if (range) {
    let [start, end] = range.replace(/bytes=/, "").split("-");
    start = parseInt(start, 10);
    end = end ? parseInt(end, 10) : size - 1;
    // 206 means serving a partial content
    res.writeHead(206, {
      "Content-Range": `bytes ${start}-${end}/${size}`,
      "Accept-Ranges": "bytes",
      "Content-Length": end - start + 1,
      "Content-Type": "video/mp4"
    });
    // read a stream with start and end
    // this is most important line that process range
    createReadStream(fileName, { start, end }).pipe(res);
  } else {
    res.writeHead(200, {
      "Content-Length": size,
      "Content-Type": "video/mp4"
    });
    createReadStream(fileName).pipe(res);
  }
}).listen(3000, () => console.log("Listening to port 3000"));
