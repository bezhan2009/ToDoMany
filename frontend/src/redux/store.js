import { configureStore, getDefaultMiddleware } from "@reduxjs/toolkit";
import thunkMiddleware from "redux-thunk";

import rootReducer from "./rootReducer";

const middleware = [...getDefaultMiddleware(), thunkMiddleware];

const store = configureStore({
  reducer: rootReducer,
  middleware,
});

export default store;