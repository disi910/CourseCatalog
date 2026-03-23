import axios from "axios";

// In production, nginx proxies /coursecatalog/api/ to the FastAPI container
// Using a relative path means it works both locally and in production
const API_URL = '/coursecatalog/api';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Define types for better TypeScript support
interface CourseFilters {
  department?: string;
  level?: string;
  language?: string;
  semester?: string;
  search?: string;
}

export const api = {
  // Get all courses with optional filters
  getCourses: async (filters?: CourseFilters) => {
    try {
      // Build query string from filters
      const params = new URLSearchParams();
      if (filters) {
        Object.entries(filters).forEach(([key, value]) => {
          if (value) params.append(key, value);
        });
      }
      
      const response = await apiClient.get(`/courses/?${params}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching courses:', error);
      throw error;
    }
  },

  // Get single course
  getCourse: async (id: string) => {
    const response = await apiClient.get(`/courses/${id}`);
    return response.data;
  },

  // Get course dependencies for visualization
  getCourseDependencies: async (id: string) => {
    const response = await apiClient.get(`/courses/${id}/dependencies`);
    return response.data;
  }
};