import createAction from "@reduxjs/toolkit";
import { api } from "../core/service/api";
import { updateReducerAction } from "./reducers";

/**
 *  Sample dispatching requests
 *  @param payload: Object
 *  - addRequestAction(payload)
 *  Sample action that changes the reducer because of already setup saga
 *  that handles action of type `REQUEST`
 */
export const addRequestAction = (payload) => ({
  type: "REQUEST",
  method: api.getApi().post,
  route: "/post/route",
  resultReducerAction: updateReducerAction,
  payload,
});

/** Create your own action type and saga
 *  that handles this action.
 */
export const refreshUserAfterDeleteAction = createAction(
  "REQUEST_REFRESH_USER_AFTER_DELETE",
);

/** See `src/store/request.saga.js` to know what type of actions are automatically handled. */
