import axios from "axios";
import { API_BASE_URL } from '../Utils/constants'
import { getCookie } from '../Utils/helper'


export const gptResponse = async (chat_id, content) => {
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

export const allChatHistory = async () => {
    try {
        debugger
        const response = await axios.get(`${API_BASE_URL}/chat_history/user`, {
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


export const chatHistory = async (chat_id) => {
    try {
        debugger
        const response = await axios.get(`${API_BASE_URL}/chat_history/chat?chat_id=${chat_id}`, {
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${getCookie()}`
            },
        });
        return response.data.messages;
    } catch (error) {
        console.error("Error during login", error);
        throw error;
    }
};

export const deleteChatHistory = async (chat_id) => {
    // todo
    try {
        debugger
        const response = await axios.get(`${API_BASE_URL}/chat_history/chat?chat_id=${chat_id}`, {
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${getCookie()}`
            },
        });
        return response.data.messages;
    } catch (error) {
        console.error("Error during login", error);
        throw error;
    }
};

export const saveMessage = async (chatId, message) => {
    debugger
    const payload = {
        chat_id: chatId,
        message: {
            content: message,
            role: "bot"
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