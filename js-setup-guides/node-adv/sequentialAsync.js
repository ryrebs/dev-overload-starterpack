// Sequential execution using async/await

const delay = (seconds) =>
  new Promise((resolves) => {
    setTimeout(() => resolves(), seconds * 1000);
  });

const sequential = async (seconds) => {
  try {
    console.log("Start waiting");
    await delay(2);
    console.log("Awaited for 2");
    await delay(seconds + 1);
    console.log(`Awaited for ${seconds + 1}`);
    await delay(seconds + 2);
    console.log(`Awaited for ${seconds + 2}`);
    console.log("Done waiting");
  } catch (err) {
    console.log(err);
  }
};

sequential(5);
