const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

if (!API_BASE_URL) {
  throw new Error(
    'REACT_APP_API_BASE_URL не задан. ' +
    'Проверьте frontend/.env и перезапустите npm start.'
  );
}

export { API_BASE_URL };