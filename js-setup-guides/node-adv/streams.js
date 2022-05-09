const fs = require("fs");
const http = require("http");
const file = "./sample.mp4";

http
  .createServer((req, res) => {
    res.writeHeader(200, { "Content-type": "video/mp4" });
    // send data by chunk using stream
    fs.createReadStream(file)
      .pipe(res)
      .on("error", console.error);
  })
  .listen(3000, console.log("Listening at port 3000"));

// scavenge garbage collector
