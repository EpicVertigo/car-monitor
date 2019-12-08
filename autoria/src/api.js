import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/',
  responseType: 'json',
});

api.defaults.xsrfCookieName = 'csrftoken';
api.defaults.xsrfHeaderName = 'X-CSRFToken';

export default api;
