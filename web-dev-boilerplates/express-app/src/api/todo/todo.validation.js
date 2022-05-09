import Joi from "joi";

const ToDoSchema = Joi.object({
  title: Joi.string(),
  description: Joi.string(),
})
  .when(Joi.ref("$action"), {
    is: "PUT",
    then: Joi.object({
      title: Joi.string().required(),
      description: Joi.string().required(),
    }),
  })
  .when(Joi.ref("$action"), {
    is: "POST",
    then: Joi.object({
      title: Joi.string().required(),
      description: Joi.string().required(),
    }),
  });

export default ToDoSchema;
