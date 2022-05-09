// Callback pattern
console.log("Start Ticking");

// Async with promise (micro tasks)
const promiseHideString = str =>
  new Promise(resolves => {
    resolves(str.replace(/[a-zA-Z]/g, "p"));
  });
promiseHideString("Replace me immediately").then(str => {
  console.log("Replaced immediately using promise: ", str);
});

// Synchronous
// continuation passing style
const hideString = (str, done) => done(str.replace(/[a-zA-Z]/g, "Y"));
// pass the done callback
hideString("Replace me immediately", str => {
  console.log("Replaced immediately: ", str);
});

// Asynchronous I
const asyncHideString = (str, done) => {
  // Invoke on next loop on event loop
  process.nextTick(() => {
    done(str.replace(/[a-zA-Z]/g, "Z"));
  });
};
asyncHideString("Replace me later", str =>
  console.log("Replaced at next tick: ", str)
);

// Asynchronous II with setTimeout
const delay = (seconds, callback) => {
  // Minimum wait time before pushing to queue for stack execution
  setTimeout(callback, seconds * 1000); // task, see also micro task
};

// Nested or sequential
delay(3, () => console.log("Wait at minimum 3 seconds"));
delay(1, () => {
  console.log("Wait at minimum 1 second");
  delay(1, () => {
    console.log("Wait at minimum 2 seconds");
  });
});

// ---
console.log("Done Ticking");

// Start Ticking
// Replaced immediately:  YYYYYYY YY YYYYYYYYYYY
// Done Ticking
// Replaced at next tick:  ZZZZZZZ ZZ ZZZZZ
// Replaced immediately using promise:  ppppppp pp ppppppppppp
// Wait at minimum 1 second
// Wait at minimum 2 seconds
// Wait at minimum 3 seconds
