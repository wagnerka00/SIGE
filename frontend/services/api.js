// Centraliza as chamadas HTTP ao backend Flask via Axios.
// Ajuste o API_BASE_URL se seu backend rodar em outra porta/host.
const API_BASE_URL =
  window.__SIGE_API_BASE_URL__ || "http://localhost:5000/api";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("sige_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error?.response?.status === 401) {
      // Token inválido/expirado: forçar logout.
      localStorage.removeItem("sige_token");
      localStorage.removeItem("sige_user");
      if (!window.location.pathname.includes("login.html")) {
        window.location.href = "./pages/login.html";
      }
    }
    return Promise.reject(error);
  }
);

const ApiService = {
  async get(path, params) {
    const { data } = await api.get(path, { params });
    return data;
  },
  async post(path, body) {
    const { data } = await api.post(path, body);
    return data;
  },
  async put(path, body) {
    const { data } = await api.put(path, body);
    return data;
  },
  async delete(path, params) {
    const { data } = await api.delete(path, { params });
    return data;
  },
};

