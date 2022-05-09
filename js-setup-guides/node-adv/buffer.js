const fs = require("fs");
const http = require("http");
const file = "./sample.mp4";

http
  .createServer((req, res) => {
    fs.readFile(file, (error, data) => {
      if (error) {
        console.log(error);
      }

      res.writeHeader(200, { "Content-Type": "video/mp4" });
      // send data as a whole using buffer
      res.end(data);
    });
  })
  .listen(3000, () => console.log("Listening at port 3000"));

// start server with garbage collection tracing: Mark sweep collector
// node --trace_gc buffer.js
