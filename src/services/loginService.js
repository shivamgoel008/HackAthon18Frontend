import axios from "axios";
import { API_BASE_URL } from '../Utils/constants'

// API call for login
export const login = async (username, password) => {
    const payload = { username, password };
    try {
        const response = await axios.post(`${API_BASE_URL}/login`, payload, {
            headers: { "Content-Type": "application/json" },
        });
        return response.data;
    } catch (error) {
        console.error("Error during login", error);
        throw error;
    }
};

export const register = async (username, password) => {
    const payload = { username, password };
    try {
        debugger
      const response = await axios.post(`${API_BASE_URL}/register`, payload, {
        headers: { "Content-Type": "application/json" },
      });
      return response.data;
    } catch (error) {
      console.error("Error during login", error);
      throw error;
    }
  };