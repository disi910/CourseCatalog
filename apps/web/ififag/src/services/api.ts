import axios from "axios";

const API_URL = 'http://localhost:8000';

export const api = {
    getCourses: async () => {
        const response = await axios.get(`${API_URL}/courses`);
        return response.data;
    }
};