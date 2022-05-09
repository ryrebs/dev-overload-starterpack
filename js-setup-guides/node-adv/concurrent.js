const logUpdate = require("log-update");
// Running concurrent but not simultaneous/ not  parallel
// See promise.all for parallel execution
const delay = (seconds) =>
  new Promise((resolves) => {
    setTimeout(
      () => resolves(`Resolves in second/s: ${seconds}`),
      seconds * 1000
    );
  });

const tasks = [delay(1), delay(2), delay(3), delay(4), delay(5)];
const toX = (x) => x;

class PromiseQueue {
  constructor(promises = [], concurrentCount = 1) {
    this.promises = promises;
    this.size = promises.length;
    this.runCount = concurrentCount;
    this.running = [];
    this.complete = [];
  }

  get runAnother() {
    return this.running.length < this.runCount && this.promises.length;
  }

  graphTasks() {
    const { promises, running, complete } = this;
    logUpdate(`
        runCount: ${this.runCount}
        todo: [${promises.map(toX)}]
        running: [${running.map(toX)}]
        complete: [${complete.map(toX)}]
    `);
  }

  run() {
    try {
      while (this.runAnother) {
        // remove one
        var promise = this.promises.shift();
        promise.then((res) => {
          // resolved remove from running
          // push to complete
          console.log(`Resolving in ${res}`);
          this.complete.push(this.running.shift());
          this.graphTasks(); // logger
          this.run(); // chained call
        });
        this.running.push(promise);
      }
    } catch (err) {
      console.error(err);
    }
  }
}

var delayQueue = new PromiseQueue(tasks, 2);
delayQueue.run();
