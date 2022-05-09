import express from "express";
import morgan from "morgan";
import compress from "compression";
import cors from "cors";
import helmet from "helmet";
import router from "../api";
import { logs } from "./vars";
import errorHandler from "../middlewares/errors";
import loggerFile from "./logger";

/**
 * Express instance
 * @public
 */
const app = express();

// formats: dev|combined
// Pass the streams to winston logging and log it as info
app.use(morgan(logs, { stream: loggerFile.stream }));

// parse body params and attach them to req.body
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// gzip compression
app.use(compress());

// secure apps by setting various HTTP headers
app.use(helmet());

// enable CORS - Cross Origin Resource Sharing
app.use(cors());

// mount api v1 routes
app.use("/api/v1", router);

// error handlers
app.use(errorHandler.notFound);
app.use(errorHandler.ajaxRequest);
app.use(errorHandler.catchAll);

module.exports = app;
