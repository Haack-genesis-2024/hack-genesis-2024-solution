import httpClient from "./httpClient";

const getFiles = () =>
  httpClient.get<string[]>("/files").then((res) => res.data);

const uploadFile = (formData: FormData) =>
  httpClient.post("/files", formData).then((res) => res.data);

const deleteFile = (fileName: string) =>
  httpClient.delete(`/files/${fileName}`).then((res) => res.data);

const filesApi = {
  getFiles,
  uploadFile,
  deleteFile,
};

export default filesApi;
