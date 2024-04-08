import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const todoApi = createApi({
  reducerPath: "todoApi",
  baseQuery: fetchBaseQuery({ baseUrl: "https://localhost:8000/" }),
  endpoints: (builder) => ({
    getAllData: builder.query({
      query: () => "/",
    }),
  }),
});

export const { useGetAllDataQuery } = todoApi;
