const env = process.env.REACT_APP_ENV;

let api_url = '';

if (env === 'production') {
    api_url = `https://${process.env.REACT_APP_DOMAIN_PROD}`;
} else if (env === 'staging') {
    api_url = `https://${process.env.REACT_APP_DOMAIN_STAG}`;
} else {
    api_url = `http://${process.env.REACT_APP_DOMAIN_DEV}`;
}

export const API_ENDPOINT_URL = api_url;