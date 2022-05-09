import httpStatus from 'http-status';
import logger from '../config/logger';

/**
 * Error handler.
 * @public
 */
exports.notFound = (req, res, next) => {
  const err = {
    message: 'Not Found',
    status: httpStatus.NOT_FOUND,
  };
  next(err);
};

exports.ajaxRequest = (err, req, res, next) => {
  if (req.xhr) {
    res.status(httpStatus.INTERNAL_SERVER_ERROR).send({ error: 'Something failed!' });
  } else {
    next(err);
  }
};

exports.catchAll = (err, req, res, next) => {
  const error = { ...err };

  if (!error.status) error.status = httpStatus.INTERNAL_SERVER_ERROR;
  // pass error when response is already written
  // to express default handler
  if (res.headersSent) {
    return next(error);
  }

  // log to file
  // logger.info({ ...resp });

  res.status(error.status).send(error);
};

exports.allowOnly = methods => (req, res) => {
  res.setHeader('ALLOW', methods);
  res.status(405).send();
};
