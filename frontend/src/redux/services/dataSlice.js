import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const todoApi = createApi({
  reducerPath: "todoApi",
  baseQuery: fetchBaseQuery({
    baseUrl: "http://127.0.0.1:8000/",
    prepareHeaders: (headers, { getState }) => {
      // const token = getState().auth.token;
      /* 
        Нужно вставить токен я не смог его найти :( 
        Так вроде б API работает?
      */
      const fakeToken = "Zm1zZWh3ZHU6ZFFmV3JHeG1GOHZPMVM2MFN4dGdRalRLWXRTUThfNWo=";

      if (fakeToken) {
        headers.set("authorization", `Bearer ${fakeToken}`);
      }

      return headers;
    },
  }),
  endpoints: (builder) => ({
    getAllData: builder.query({
      query: () => "/api/environment/",
    }),
  }),
});

export const { useGetAllDataQuery } = todoApi;
