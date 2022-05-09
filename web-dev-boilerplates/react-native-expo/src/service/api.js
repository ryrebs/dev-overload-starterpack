import axios from "axios";
import Constants from "expo-constants";

const TIMEOUT = 60 * 1000;
const NETWORK_ERROR_MSG = "Network Error. Please try again";
const REQUEST_TIMEOUT_MSG = "Request Timeout";
const ERROR_WITH_STATUS = "Request Timeout";
const SOMETHING_WENT_WRONG_MSG = "Something Went Wrong. Please Try Again.";
const API_HOST = Constants.manifest.extra.EXPO_API;

/* eslint-disable max-classes-per-file */
import Constants from "expo-constants";

const transformResponse = (response) => {
  // We want the api to response with these keys
  // otherwise throw an error
  const { status, message, data } = response;
  if (
    response.hasOwnProperty("status") &&
    response.hasOwnProperty("message") &&
    response.hasOwnProperty("data")
  )
    return {
      status,
      message,
      data,
    };
  else if (Constants.manifest.extra.EXPO_ENV === "dev")
    throw new Error("keys: status, message, data, should be present");
  else throw new Error(SOMETHING_WENT_WRONG_MSG);
};

const successResponseInterceptor = (response) => {
  const result = response.data;
  return transformResponse(result);
};

const errorResponseInterceptor = (error) => {
  let response;
  if (error.response) {
    // transform all non 2xx errors
    const responseObj = error.response.data;
    if (responseObj && responseObj instanceof Object)
      response = { ...responseObj };
    else
      response = {
        data: null,
        message: `${ERROR_WITH_STATUS}: ${error.response.status}`,
        status: null,
      };
  } else if (error.request) {
    // The request was made but no response was received
    if (error.request._timedOut)
      response = { data: null, message: REQUEST_TIMEOUT_MSG, status: null };
    else
      response = { data: null, message: error.request._response, status: null };
  } else {
    // catch errors before a response
    response = {
      data: null,
      message: error.message || NETWORK_ERROR_MSG,
      status: null,
    };
  }
  return Promise.reject(transformResponse(response));
};

const createAxiosInstance = (url) => {
  const axiosApi = axios.create({
    baseURL: url,
    timeout: TIMEOUT,
  });
  axiosApi.interceptors.response.use(
    successResponseInterceptor,
    errorResponseInterceptor
  );
  axiosApi.defaults.headers.common.Accept = "application/json; charset=utf-8";
  return axiosApi;
};

export const api = (() => {
  // eslint-disable-next-line no-underscore-dangle
  let _api;
  return {
    initialize: (apiInst) => {
      if (_api === undefined) _api = apiInst;
    },
    getApi: () => {
      if (_api !== null) return _api;
      throw Error("Initialize api first.");
    },
  };
})();

export const setBearerToken = (token) => {
  // eslint-disable-next-line no-param-reassign
  api.getApi().defaults.headers.common.Authorization = token;
};

export default () => {
  api.initialize(createAxiosInstance(API_HOST));
};
