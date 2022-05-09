const path = require("path");

/** imports .env variables
 *  .env.sample should include the environment variables needed in .env *without values*
 *  .env should have all *variables* and *values* needed in .env.sample
 */
require("dotenv-safe").load({
  path: path.join(__dirname, "../../.env"),
  sample: path.join(__dirname, "../../.env.example"),
});

/** .env is overriden by explicitly setting environment in package.json */
module.exports = {
  env: process.env.NODE_ENV,
  port: process.env.PORT,
  jwtSecret: process.env.JWT_SECRET,
  jwtExpirationInterval: process.env.JWT_EXPIRATION_MINUTES,
  mongo: {
    uri:
      process.env.NODE_ENV === "test"
        ? process.env.MONGO_URI_TESTS
        : process.env.MONGO_URI,
  },
  logs: process.env.NODE_ENV === "production" ? "combined" : "dev",
};
