import axios from 'axios';

// IMPORTANT, change this into a non local domain in production
const BASE_URL = 'http://localhost:8000/api/v1';
const ACCESS_TOKEN = 'access_token';
const REFRESH_TOKEN = 'refresh_token';

const tokenRequest = axios.create({
  baseURL: BASE_URL,
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
    accept: 'application/json'
  },
});

const loginUser = (username, password) => {
  const loginBody = {
    username,
    password
  }
  return tokenRequest.post('/jwt/create/', loginBody)
    .then((response) => {
      window.localStorage.setItem(ACCESS_TOKEN, response.data.access)
      window.localStorage.setItem(REFRESH_TOKEN, response.data.refresh)
    }).catch((error) => {
      console.log(error)
      return Promise.reject(error)
    })
};

const refreshToken = () => {
  const refreshBody = {
    refresh: window.localStorage.getItem(REFRESH_TOKEN)
  }

  return tokenRequest.post('/jwt/refresh/', refreshBody)
    .then((response) => {
      window.localStorage.setItem(ACCESS_TOKEN, response.data.access)
      return Promise.resolve(response.data)
    }).catch((error) => {
      console.log(error)
      return Promise.reject(error)
    })
};

/*
 * authRequest
 *
 * This refreshes the request and retries the token if it is invalid.
 * This is what you use to create any requests that need the Tokens.
 * In other word please use if the request needed to be done by an authenticated user.
 *
 * Example:
 *     authRequest.get('/path/to/endpoint/',extraParameters)
 *        .then(response=>{
 *          // do something with successful request
 *        }).catch((error)=> {
 *          // handle any errors.
 *        });
 */
const authRequest = axios.create({
  baseURL: BASE_URL,
  timeout: 5000,
  headers: {
    Authorization: `JWT ${window.localStorage.getItem(ACCESS_TOKEN)}`,
    'Content-Type': 'application/json',
  },
});

const logoutUser = () => {
  window.localStorage.removeItem(ACCESS_TOKEN);
  window.localStorage.removeItem(REFRESH_TOKEN);
  authRequest.defaults.headers.Authorization = '';
}

const isCorrectRefreshError = (status) => status === 401;

const errorInterceptor = (error) => {
  const originalRequest = error.config;
  const {
    status
  } = error.response;

  if (isCorrectRefreshError(status)) {
    return refreshToken().then(() => {
      const headerAuthorization = `Bearer ${window.localStorage.getItem(ACCESS_TOKEN)}`;
      authRequest.defaults.headers.Authorization = headerAuthorization;
      originalRequest.headers.Authorization = headerAuthorization;
      return authRequest(originalRequest);
    }).catch((tokenRefreshError) => {
      // if token refresh fails, logout the user to avoid potential security risks.
      logoutUser();
      return Promise.reject(tokenRefreshError);
    });
  }
  return Promise.reject(error);
};

authRequest.interceptors.response.use(
  (response) => response, // this is for all successful requests.
  (error) => errorInterceptor(error), // handle the request
);

export {
  tokenRequest,
  loginUser,
  logoutUser,
  refreshToken,
  authRequest,
  errorInterceptor,
  BASE_URL,
  ACCESS_TOKEN,
  REFRESH_TOKEN,
};
