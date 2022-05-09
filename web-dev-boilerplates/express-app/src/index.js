import { port, env } from "./config/vars";
import logger from "./config/logger";
import app from "./config/express";

if (process.env.NODE_ENV !== "test")
  app.listen(port, () => {
    logger.info(`Server started on port ${port} (${env})`);
  });

module.exports = app;
