import React, { useState, useEffect } from 'react';
import Conversation from './Conversation';
import Messages from './Messages';
import { v4 as uuidv4 } from 'uuid';
import { allChatHistory, gptResponse } from '../services/chatService';
import { formatDistanceToNow } from 'date-fns';

const Chat = () => {
    const [data, setData] = useState([]);
    const [selectedChatId, setSelectedChatId] = useState(null);

    const fetchChatHistory = async () => {
        try {
            const response = await allChatHistory();
            // sort in descending order: newest first
            const sortedResponse = response.sort((a, b) => {
                const aTime = new Date(a.messages[0].timestamp);
                const bTime = new Date(b.messages[0].timestamp);

                return bTime - aTime;
            });
            const modifiedData = sortedResponse.map((item) => ({
                chatId: item.chat_id,
                time: formatDistanceToNow(new Date(item.messages[0].timestamp), {
                    addSuffix: true,
                }),
                message: item.messages[0].content,
            }));
            setData([...modifiedData]);
        } catch (error) {
            console.error("Error fetching chat history:", error);
        }
    };

    useEffect(() => {
        fetchChatHistory();
    }, []); // fetch chat history on initial render

    const handleNewChatClick = async () => {
        const chat_id = uuidv4();
        try {
            await gptResponse(chat_id, "hey bitch lodu");
            fetchChatHistory(); // re-fetch chat history after creating a new chat
            setSelectedChatId(chat_id)
        } catch (error) {
            console.error("Error creating new chat:", error);
        }
    };

    const handleChatSelect = (chatId) => {
        setSelectedChatId(chatId);
    };

    return (
        <div className="">
            <div className="flex bg-white dark:bg-gray-900">
                <div className="w-80 h-screen dark:bg-gray-800 bg-gray-100 p-2 hidden md:block">
                    <div className="h-full overflow-y-auto">
                        <div className="text-xl font-extrabold text-gray-600 dark:text-gray-200 p-3">ChatGpt</div>
                        <div className="flex justify-between">
                            <div className="text-lg font-semibol text-gray-600 dark:text-gray-200 p-3">Recent</div>
                            <div
                                className="text-lg font-semibol text-gray-600 dark:text-gray-200 p-3 cursor-pointer"
                                onClick={handleNewChatClick}
                            >
                                New Chat
                            </div>
                        </div>
                        <Conversation data={data} onClick={handleChatSelect} />
                    </div>
                </div>
                <div className="flex-grow h-screen p-2 rounded-md">
                    <Messages chatId={selectedChatId} />
                </div>
            </div>
        </div>
    );
};

export default Chat;
