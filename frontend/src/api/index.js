import axios from 'axios';
import { API_ENDPOINT_URL } from './api';

export default axios.create({
    baseURL: API_ENDPOINT_URL
});