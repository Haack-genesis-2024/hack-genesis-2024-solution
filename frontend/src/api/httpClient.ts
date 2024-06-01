import axios from "axios";

const baseUrl = import.meta.env.VITE_API_BASE_URL;

const httpClient = axios.create({
  baseURL: baseUrl,
  withCredentials: true,
});

export default httpClient;
