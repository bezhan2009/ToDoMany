import { combineReducers } from "@reduxjs/toolkit";
import { todoApi } from "./services/dataSlice";
import menuOpenSlice from "./slices/menuOpenSlice";

const rootReducer = combineReducers({
  [todoApi.reducerPath]: todoApi.reducer,
  menuOpen: menuOpenSlice,
});

export default rootReducer;
