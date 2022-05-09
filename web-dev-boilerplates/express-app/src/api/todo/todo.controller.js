import { SuccessResponse, CreatedResponse } from "../models/Response.model";
import Todo from "./Todo.model";

const add = (req, res, next) => {
  const todo = new Todo(req.body).save();
  const response = new CreatedResponse("Todos", todo);
  res.status(response.status).send(response.toString());
};

const get = (req, res, next) => {
  const { todoId } = req.params;
  const response = new SuccessResponse("Todos", Todo.findOne(todoId));
  res.status(response.status).send(response.toString());
};

const getAll = (req, res, next) => {
  const results = Todo.findAll();
  const response = new SuccessResponse("Todos", results);
  res.status(response.status).send(response.toString());
};

const update = (req, res, next) => {
  const { todoId } = req.params;
  const payload = req.body;
  const response = new SuccessResponse("Todos", Todo.update(todoId, payload));
  res.status(response.status).send(response.toString());
};

const remove = (req, res, next) => {
  const { todoId } = req.params;
  const response = new SuccessResponse("Todos", Todo.delete(todoId));
  res.status(response.status).send(response.toString());
};

export { add, get, getAll, update, remove };
