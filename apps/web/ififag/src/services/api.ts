import axios from "axios";
import type { Course, FilterOptions, DependencyGraph } from "../types";

// VITE_API_URL allows overriding for local dev (e.g. http://localhost:8000)
// In production, nginx proxies /coursecatalog/api/ to the FastAPI container
const API_URL = import.meta.env.VITE_API_URL || '/coursecatalog/api';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  getCourses: async (filters?: FilterOptions & { search?: string }): Promise<Course[]> => {
    const params = new URLSearchParams();
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value) params.append(key, value);
      });
    }
    const response = await apiClient.get(`/courses/?${params}`);
    return response.data;
  },

  getCourse: async (id: string): Promise<Course> => {
    const response = await apiClient.get(`/courses/${id}`);
    return response.data;
  },

  getCourseDependencies: async (id: string): Promise<DependencyGraph> => {
    const response = await apiClient.get(`/courses/${id}/dependencies`);
    return response.data;
  },

  getPrerequisiteCounts: async (): Promise<Record<string, number>> => {
    const response = await apiClient.get('/courses/prerequisite-counts');
    return response.data;
  },
};
