import React, { useState, useEffect } from 'react';
import Conversation from './Conversation';
import Messages from './Messages';
import { v4 as uuidv4 } from 'uuid';
import { allChatHistory, gptResponse,deleteChatHistory, saveMessage } from '../services/chatService';
import { formatDistanceToNow } from 'date-fns';
import Header from './Header';
import {APPLICATION_NAME} from '../Utils/constants'
import { getCookie, getSubjectFromJwt, getTextBeforeAt } from '../Utils/helper';
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
            const username = getTextBeforeAt(getSubjectFromJwt(getCookie()));
            await saveMessage(chat_id, "Hi "+username+", How can i help you");
            fetchChatHistory(); // re-fetch chat history after creating a new chat
            setSelectedChatId(chat_id)
        } catch (error) {
            console.error("Error creating new chat:", error);
        }
    };

    const handleChatSelect = (chatId) => {
        setSelectedChatId(chatId);
    };

    const handleChatDelete=(chatId) =>{
        //todo
        deleteChatHistory(chatId);
    }

    return (
        <div className="h-screen flex flex-col">
            <div className="">
                <Header />
            </div>
            <div className="flex flex-grow overflow-hidden  mt-px bg-white dark:bg-[#171717]">
            <div className="w-80 h-full  p-2 hidden md:block ">
                    <div className="h-full overflow-y-auto">
                        <div className="text-xl font-extrabold text-white p-3">{APPLICATION_NAME}</div>
                        <div className="flex justify-between">
                            <div className="text-lg font-semibold text-white p-3">Recent</div>
                            <div
                                className="text-lg font-semibold text-white p-3 cursor-pointer hover:text-gray-300"
                                onClick={handleNewChatClick}
                            >
                                New Chat
                            </div>
                        </div>
                        <Conversation data={data} onClick={handleChatSelect} onDelete={handleChatDelete}/>
                    </div>
                </div>
                <div className="flex-grow h-full p-2 rounded-md overflow-y-auto">
                    <Messages chatId={selectedChatId} />
                </div>
            </div>
        </div>
    );
};

export default Chat;
