import { combineReducers } from '@reduxjs/toolkit';
import dataReducer from './slices/dataSlice';

const rootReducer = combineReducers({
  data: dataReducer,
});

export default rootReducer;
