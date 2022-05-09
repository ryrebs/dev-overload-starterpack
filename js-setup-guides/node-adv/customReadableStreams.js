const { Readable } = require("stream");

const cards = ["Heart", "Spade", "Flower", "Diamond"];

class StreamFromArray extends Readable {
  constructor(array = []) {
    // 1. Read with Binary mode as binary or string pass an encoding
    // super({ encoding: "utf-8" });
    // 2. Read with objectMode reads object
    // or Object mode
    super({ objectMode: true });
    this.array = array;
    this.index = 0;
  }

  // Override
  _read() {
    if (this.index <= this.array.length - 1) {
      // create the chunk to be read
      const chunk = {
        data: this.array[this.index],
        index: this.index,
      };
      // push the created chunk to be read
      this.push(chunk);

      // increment index to next data
      this.index += 1;
    } else {

      // signals no readable left
      this.push(null);
    }
  }
}

const cardStream = new StreamFromArray(cards);

// Read and listen to data event
cardStream.on("data", (chunk) => console.log(chunk));

// listen to end event
cardStream.on("end", () => console.log("Done reading."));

// { data: 'Heart', index: 0 }
// { data: 'Spade', index: 1 }
// { data: 'Flower', index: 2 }
// { data: 'Diamond', index: 3 }
