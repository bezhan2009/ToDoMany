import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import axios from "axios";

export const fetchAPIData = createAsyncThunk(
  'data/fetchAPIData',
  async () => {
    const response = await axios.get("http://localhost:8000/");
    return response.data;
  }
);

const dataSlice = createSlice({
  name: "data",
  initialState: {
    data: [],
    error: null,
    isLoading: false,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchAPIData.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(fetchAPIData.fulfilled, (state, action) => {
        state.isLoading = false;
        state.data = action.payload;
      })
      .addCase(fetchAPIData.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message;
      });
  },
});

export default dataSlice.reducer;
