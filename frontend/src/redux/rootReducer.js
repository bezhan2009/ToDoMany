import { combineReducers } from "@reduxjs/toolkit";
import { todoApi } from "./services/dataSlice";
import menuOpenSlice from "./slices/menuOpenSlice";

const rootReducer = combineReducers({
  menuOpen: menuOpenSlice,
  [todoApi.reducerPath]: todoApi.reducer,
});

export default rootReducer;
