import axios from "axios";


const response = axios.create({
  baseURL: "http://localhost:8000/",
});

axios.get("/");

export default response;

