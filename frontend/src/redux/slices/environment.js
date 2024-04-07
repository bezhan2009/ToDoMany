import { createSlice } from '@reduxjs/toolkit';

export const dataSlice = createSlice({
  name: 'data',
  initialState: {
    isLoading: false,
    error: null,
    data: null,
  },
  reducers: {
    fetchDataStart: (state) => {
      state.isLoading = true;
      state.error = null;
      state.data = null;
    },
    fetchDataSuccess: (state, action) => {
      state.isLoading = false;
      state.data = action.payload;
    },
    fetchDataFailure: (state, action) => {
      state.isLoading = false;
      state.error = action.payload;
    },
  },
});

export const { fetchDataStart, fetchDataSuccess, fetchDataFailure } = dataSlice.actions;

export default dataSlice.reducer;
