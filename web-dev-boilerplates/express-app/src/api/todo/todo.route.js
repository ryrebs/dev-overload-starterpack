import express from "express";
import { get, getAll, add, update, remove } from "./todo.controller";
import errorMiddleware from "../../middlewares/errors";
import validationMiddleware from "../../middlewares/validation";
import ToDoSchema from "./todo.validation";

const router = express.Router();

/**
 * @api {get} /api/v1 Get message
 * @apiName GetRoot
 * @apiGroup Root
 * @apiDescription Testing if api is running and working.
 * @apiPermission none
 * @apiSuccess {String} message Default return message
 * @apiExample {curl} Example usage:
 *     curl -i http://localhost:5000/api/v1/
 * @apiSuccessExample {json} Success-Response:
 *     HTTP/1.1 200 OK
 *     {
 *       "message": "Minimal boilerplate in express",
 *     }
 */
router.route("/").get((req, res) => {
  res.status(200).send({ message: "Minimal boilerplate in express" });
});

router
  .route("/todos")
  /**
   * @api {get} api/v1/todos Get all
   * @apiName GetTodos
   * @apiGroup Todos
   * @apiDescription Return all existing todos in the database.
   * @apiPermission none
   * @apiSuccess (200) {Object[]} data contains Array of todo objects
   * @apiSuccess (200) {Number} data.title contains return status
   * @apiSuccess (200) {String} data.description contains a  return message
   * @apiExample {curl} Example usage:
   *     curl -i http://localhost:5000/api/v1/todos
   * * @apiSuccessExample {json} Success-Response:
   *     HTTP/1.1 200 OK
   *     {
   *       "message": "Todos",
   *       "status": 200,
   *       "data": [
   *          {
   *              title: "My todo",
   *              description: "Get it done later"
   *          },
   *        ]
   *     }
   */
  .get(getAll)
  /** @api {post} api/v1/todos Post todos
   * @apiName PostTodos
   * @apiGroup Todos
   * @apiDescription Create new todo
   * @apiPermission none
   * @apiParam (Parameters) {String} title Your todo title
   * @apiParam (Parameters) {String} description Your todo description
   * @apiSuccess (Created 201) {Object[]} data contains Array of todo objects
   * @apiSuccess (Created 201) {Number} data.title contains return status
   * @apiSuccess (Created 201) {String} data.description contains a  return message
   * @apiExample {curl} Example usage:
   *     curl -d '{title: "My todo", description: "Get it done later"}' -H 'Content-Type: application/json' http://localhost:5000/api/v1/todos
   * @apiSuccessExample {json} Success-Response:
   *     HTTP/1.1 201 OK
   *     {
   *       "message": "Todos",
   *       "status": 200,
   *       "data": [
   *          {
   *              title: "My todo",
   *              description: "Get it done later"
   *          },
   *        ]
   *     }
   */
  .post(validationMiddleware.validate({ action: "POST" }, ToDoSchema), add)
  .all(errorMiddleware.allowOnly(["GET", "POST"]));

router
  .route("/todos/:todoId")
  /** @api {get} api/v1/:todoId Get one
   * @apiName GetTodo
   * @apiGroup Todos
   * @apiDescription Returns a single todo
   * @apiError (Errors) {Object[]} data The <code>todoId</code> is not found. Returns an empty array [].
   * @apiErrorExample {json} Error-Response:
   *     HTTP/1.1 404 Not Found
   *     {
   *       "data": []
   *     }
   */
  .get(get)
  /** @api {put} api/v1/:todoId Put one
   * @apiName PutTodo
   * @apiGroup Todos
   * @apiDescription Updates a single todo
   * @apiPermission none
   * @apiParam (Parameters) {String} title Your todo title
   * @apiParam (Parameters) {String} description Your todo description
   * @apiExample {curl} Example usage:
   *     curl -X PUT -d '{title: "My todo", description: "Get it done later"}' -H 'Content-Type: application/json' http://localhost:5000/api/v1/todos/1
   * @apiSuccessExample {json} Success-Response:
   *     HTTP/1.1 200 OK
   *     {
   *       "message": "Todos",
   *       "status": 200,
   *       "data":
   *          {
   *              title: "My todo",
   *              description: "Get it done later"
   *          }
   *     }
   */
  .put(validationMiddleware.validate({ action: "PUT" }, ToDoSchema), update)
  .delete(remove)
  .all(errorMiddleware.allowOnly(["GET", "PUT", "DELETE"]));

module.exports = router;
