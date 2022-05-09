const delay = seconds =>
  new Promise(resolves => {
    setTimeout(() => resolves("Delay done..."), seconds * 1000);
  });

// executes at micro task processing
const sequential = seconds =>
  Promise.resolve()
    .then(() => console.log("Started"))
    .then(() => {
      console.log("Start 5 secs delay");
      return delay(5);
    })
    // Delay done...
    .then(msg => console.log(msg))
    .then(() => {
      console.log(`Start ${seconds} second/s delay`);
      return delay(seconds);
    })
    .then(msg => console.log(msg));

sequential(1);
console.log("Starting sequential");

// Starting sequential
// Started
// Delay after started
// Started already...
// Now waiting for 1 second/s
// Delay done...
