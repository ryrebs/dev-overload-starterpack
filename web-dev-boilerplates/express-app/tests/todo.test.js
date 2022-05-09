import request from "supertest";
import { expect } from "chai";
import app from "../src";

describe("Api is working", () => {
  it("Responds with 200", (done) => {
    request(app)
      .get("/api/v1")
      .set("Accept", "application/json")
      .expect(200, { message: "Minimal boilerplate in express" }, done);
  });
});

describe("Todos resource", () => {
  it("Should get empty todos", (done) => {
    request(app).get("/api/v1/todos").set("Accept", "application/json").expect(
      200,
      {
        data: [],
        message: "Todos",
        status: 200,
      },
      done
    );
  });

  it("Should create new todo", (done) => {
    request(app)
      .post("/api/v1/todos")
      .set("Accept", "application/json")
      .send({
        description: "Test todos",
        title: "Create test",
      })
      .expect((res) => {
        expect(res.body.data).to.own.include({ description: "Test todos" });
        expect(res.body.data).to.own.include({ title: "Create test" });
      })
      .expect(201, done);
  });

  it("Should return a single todo", (done) => {
    const agent = request.agent(app);

    agent
      .post("/api/v1/todos")
      .set("Accept", "application/json")
      .send({
        description: "Test todos",
        title: "Create test",
      })
      .end((err, res) => {
        if (err) return done(err);
        const id = res.body.data.$loki;
        agent
          .get(`/api/v1/todos/${id}`)
          .set("Accept", "application/json")
          .expect(200, done);
      });
  });
});
