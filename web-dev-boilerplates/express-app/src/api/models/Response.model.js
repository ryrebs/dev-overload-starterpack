import httpStatus from 'http-status';

class Response {
  constructor(message, status, data) {
    this.message = message;
    this.status = status;
    this.data = data;
  }

  toString = () => {
    const { data, status, message } = this;
    return { message, status, data };
  };
}

class CreatedResponse extends Response {
  constructor(message, data) {
    super(message, httpStatus.CREATED, data);
  }
}
class SuccessResponse extends Response {
  constructor(message, data) {
    super(message, httpStatus.OK, data);
  }
}

class DeletedResponse extends Response {
  constructor(message, data) {
    super(message, httpStatus.NO_CONTENT, data);
  }
}

class ServerErrorResponse extends Response {
  constructor(message, data) {
    super(message, httpStatus.INTERNAL_SERVER_ERROR, data);
  }
}

class BadRequestResponse extends Response {
  constructor(message, data) {
    super(message, httpStatus.BAD_REQUEST, data);
  }
}

class NotFoundResponse extends Response {
  constructor(message, data) {
    super(message, httpStatus.NOT_FOUND, data);
  }
}
class UnAuthenticatedErrorResponse extends Response {
  constructor(message, data) {
    super(message, httpStatus[401], data);
  }
}
class UnAuthorizedErrorResponse extends Response {
  constructor(message, data) {
    super(message, httpStatus[403], data);
  }
}

export {
  Response,
  ServerErrorResponse,
  CreatedResponse,
  BadRequestResponse,
  SuccessResponse,
  DeletedResponse,
  UnAuthenticatedErrorResponse,
  UnAuthorizedErrorResponse,
  NotFoundResponse,
};
