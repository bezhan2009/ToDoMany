import axios from "axios";

class API {
  static instance = axios.create({
    baseURL: "http://localhost:8000/",
  });

  static async get() {
    const response = await API.instance.get('/');
    return response.data;
  }
}

export default API;
