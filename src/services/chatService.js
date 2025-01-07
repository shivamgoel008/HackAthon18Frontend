import axios from "axios";
import { API_BASE_URL } from '../Utils/constants'
import {getCookie} from '../Utils/helper'


export const gptResponse = async (chat_id,content) => {
    debugger
    const payload = {
        chat_id: chat_id,
        message: {
            content: content,
            role: "user"
        }
    };
    try {
        const response = await axios.post(`${API_BASE_URL}/chat_history/chat`, payload, {
            headers: { 
                "Content-Type": "application/json",
                "Authorization": `Bearer ${getCookie()}` 
            },
        });
        return response.data;
    } catch (error) {
        console.error("Error during login", error);
        throw error;
    }
};