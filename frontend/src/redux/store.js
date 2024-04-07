import { configureStore } from "@reduxjs/toolkit";
import dataReducer from "./slices/environment";

const store = configureStore({
  reducer: {
    data: dataReducer,
  },
});

export default store;
