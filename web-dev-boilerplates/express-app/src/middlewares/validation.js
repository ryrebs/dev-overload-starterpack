import Joi from "joi";
import { BadRequestResponse } from "../api/models/Response.model";

const checkErrors = (result) => {
  let errorResponse;
  if (result.error) {
    const { details } = result.error;
    const errors = [];
    details.map((o) => errors.push(o.message));
    errorResponse = new BadRequestResponse("Invalid request to resource.", {
      errors,
    });
  }

  return errorResponse;
};

exports.validate = (action, schema) => (req, res, next) => {
  const result = Joi.validate(req.body, schema, {
    context: { ...action },
    abortEarly: false,
  });
  const responseErrors = checkErrors(result);
  if (responseErrors) return next(responseErrors);
  return next();
};
