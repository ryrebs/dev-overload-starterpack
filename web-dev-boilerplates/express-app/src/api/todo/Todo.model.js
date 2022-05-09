import LokiDb from "../../database";

const todos = LokiDb.getCollection();

class Todo {
  constructor(req) {
    this.title = req.title;
    this.description = req.description;
  }

  save = (req) => {
    const todo = this.buildObject();
    return todos.insert(todo);
  };

  buildObject = () => {
    const { title, description } = this;
    return { title, description };
  };

  static findAll = () => {
    return todos.data;
  };

  static findOne = (id) => {
    return todos.get(id);
  };

  static delete = (id) => {
    const todo = todos.get(id);
    return todos.remove(todo);
  };

  static update = (id, payload) => {
    const { title, description } = payload;
    let todo = todos.get(id);
    todo.title = title;
    todo.description = description;
    return todos.update(todo);
  };
}

export default Todo;
