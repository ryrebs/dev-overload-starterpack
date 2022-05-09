const winston = require("winston");
const appRoot = require("app-root-path");

const options = {
  fileError: {
    level: "error",
    filename: `${appRoot}/logs/error.log`,
    handleExceptions: true,
    json: true,
    maxsize: 5242880,
    maxFiles: 5,
    colorize: false,
  },
  fileCombine: {
    level: "info",
    filename: `${appRoot}/logs/combined.log`,
    handleExceptions: true,
    json: true,
    maxsize: 5242880,
    maxFiles: 5,
    colorize: false,
  },
  console: {
    level: "info",
    format: winston.format.simple(),
    handleExceptions: true,
    json: true,
    colorize: true,
  },
};

const errorLogger = new winston.transports.File(options.fileError);
const combinedLogger = new winston.transports.File(options.fileCombine);
const consoleLogger = new winston.transports.Console(options.console);

const loggerToFile = winston.createLogger({
  level: "info",
  format: winston.format.json(),
});

if (process.env.NODE_ENV === "production") {
  loggerToFile.add(errorLogger);
  loggerToFile.add(combinedLogger);
} else {
  loggerToFile.add(consoleLogger);
}
// Create a stream to accept morgan logs as info
// Handled by file transport who logs info and below
loggerToFile.stream = {
  write: (message) => {
    loggerToFile.info(message.trim());
  },
};

// On development log to console otherwise log to file
module.exports = loggerToFile;
