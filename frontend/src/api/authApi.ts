import httpClient from "./httpClient";

const logout = () => httpClient.post("/logout").then((res) => res.data);

const authApi = {
  logout,
};

export default authApi;
