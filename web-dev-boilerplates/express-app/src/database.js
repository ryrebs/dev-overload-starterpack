import loki from "lokijs";

const LokiDb = (() => {
  let db;
  let todosCollection;

  const initDb = () => {
    db = new loki("dev.db");
    todosCollection = db.addCollection("todos");
    return todosCollection;
  };

  return {
    getCollection: () => {
      if (!todosCollection) {
        todosCollection = initDb();
      }
      return todosCollection;
    },
  };
})();

export default LokiDb;
