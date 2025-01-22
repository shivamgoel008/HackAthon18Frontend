import React, { useEffect, useState, useRef } from 'react';
import { formatDistanceToNow } from 'date-fns';
import logo from '../logo.svg';
import { chatHistory, gptResponse, saveMessage } from '../services/chatService';
import { ReactTyped } from 'react-typed';

const Messages = ({ chatId }) => {
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);
    const [typing, setTyping] = useState(false);
    const [error, setError] = useState(null);
    const [inputValue, setInputValue] = useState("");
    const [isSending, setIsSending] = useState(false);

    const messagesEndRef = useRef(null);

    useEffect(() => {
        const fetchMessages = async () => {
            if (!chatId) return;
            setLoading(true);
            setError(null);
            setTyping(false)

            try {
                const data = await chatHistory(chatId);
                const sortedMessages = data.sort(
                    (a, b) => new Date(a.timestamp) - new Date(b.timestamp)
                );
                setMessages(sortedMessages);
            } catch (err) {
                console.error("Error fetching messages:", err);
                setError("Failed to load messages. Please try again.");
            } finally {
                setLoading(false);
            }
        };

        fetchMessages();
    }, [chatId]);

    const setTypingFalse=()=>{
        setTyping(false);
    }

    const handleSendMessage = async () => {
        if (!inputValue.trim() || isSending) return;
        setIsSending(true);
        setTyping(true);

        try {

            setInputValue("");


            const response = await gptResponse(chatId, inputValue.trim());
            await saveMessage(chatId, response.message);
            const chatIdHistory = await chatHistory(chatId)
            const sortedMessages = chatIdHistory.sort(
                (a, b) => new Date(a.timestamp) - new Date(b.timestamp)
            );
            setMessages(sortedMessages);

        } catch (err) {
            console.error("Error sending message:", err);
            setError("Failed to send message. Please try again.");
        } finally {
            setIsSending(false);
        }
    };

    useEffect(() => {
        // Auto-scroll 
        if (messagesEndRef.current) {
            messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
        }
        const scrollToBottom = () => {
            if (messagesEndRef.current) {
                messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
            }
        };
        if (typing === true) {
            const intervalId = setInterval(scrollToBottom, 1000);
            return () => clearInterval(intervalId);
        }
    }, [messages,typing]);

    if (!chatId) {
        return (
            <div className="flex items-center justify-center h-full text-gray-500 text-center">
                Select a chat to view messages.
            </div>
        );
    }

    if (loading) {
        return (
            <div className="text-gray-500 text-center p-5">
                Loading messages...
            </div>
        );
    }

    if (error) {
        return (
            <div className="text-red-500 text-center p-5">
                {error}
            </div>
        );
    }
    const renderMessage = (item, index) => {
        if (messages.length === 1) {
            return (
                <div key={index} className="flex items-end w-3/4">
                    <img className="w-8 h-8 m-3 rounded-full" src={logo} alt="avatar" />
                    <div className="p-3 mx-3 my-1 rounded-2xl rounded-bl-none sm:w-3/4 md:w-3/6 outline bg-[#303030] outline-black">
                        {
                            <ReactTyped
                                strings={[item.content]}
                                typeSpeed={10}
                                showCursor={false}
                                loop={false}
                                className=' text-white'
                                onComplete={setTypingFalse}
                            />
                        }
                        <div className="text-xs text-gray-400">
                            {formatDistanceToNow(new Date(item.timestamp), { addSuffix: true })}
                        </div>
                    </div>
                </div>
            )
        }
        if (item.role === 'user') {
            return (
                <div key={index} className="flex justify-end">
                    <div className="flex items-end w-auto m-1 rounded-xl rounded-br-none sm:w-3/4 md:w-auto outline bg-[#303030] outline-black">
                        <div className="p-2">
                            <p className="text-white">{item.content}</p>
                            <div className="flex justify-end text-xs text-gray-400">
                                {formatDistanceToNow(new Date(item.timestamp), { addSuffix: true })}
                            </div>
                        </div>
                    </div>
                </div>
            );
        } else if (item.role === 'bot' && index === messages.length - 1 && typing === true) {
            return (
                <div key={index} className="flex items-end w-3/4">
                    <img className="w-8 h-8 m-3 rounded-full" src={logo} alt="avatar" />
                    <div className="p-3 mx-3 my-1 rounded-2xl rounded-bl-none sm:w-3/4 md:w-3/6 outline bg-[#303030] outline-black">
                        {
                            <ReactTyped
                                strings={[item.content]}
                                typeSpeed={10}
                                showCursor={false}
                                loop={false}
                                className=' text-white'
                                onComplete={setTypingFalse}
                            />
                        }
                        <div className="text-xs text-gray-400">
                            {formatDistanceToNow(new Date(item.timestamp), { addSuffix: true })}
                        </div>
                    </div>
                </div>
            )
        } else {
            return (
                <div key={index} className="flex items-end w-3/4">
                    <img className="w-8 h-8 m-3 rounded-full" src={logo} alt="avatar" />
                    <div className="p-3 mx-3 my-1 rounded-2xl rounded-bl-none sm:w-3/4 md:w-3/6 outline bg-[#303030] outline-black">
                        <p className=' text-white'>{item.content}</p>
                        <div className="text-xs text-gray-400">
                            {formatDistanceToNow(new Date(item.timestamp), { addSuffix: true })}
                        </div>
                    </div>
                </div>
            );
        }
    };



    return (
        <div className="flex-grow h-full flex flex-col">
            {/* Messages List */}
            <div className="w-full flex-grow bg-[#212121] my-2 p-2 overflow-y-auto rounded-t-3xl">
                {messages.map((item, index) => renderMessage(item, index))}
                <div ref={messagesEndRef} />
            </div>

            {/* Message Input Section */}
            <div className="h-15 p-3 rounded-xl rounded-tr-none rounded-tl-none bg-[#2f2f2f]">
                <div className="flex items-center">
                    <div className="p-2 text-white">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                    </div>
                    <div className="search-chat flex flex-grow p-2">
                        <input
                            className="input text-white text-sm p-5 focus:outline-none bg-[#2f2f2f] flex-grow rounded-l-md"
                            type="text"
                            placeholder="Type your message ..."
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                            disabled={isSending}
                        />
                        <div
                            className={`bg-[#2f2f2f]  flex justify-center items-center pr-3 text-white rounded-r-md cursor-pointer ${isSending ? 'opacity-50' : ''}`}
                            onClick={handleSendMessage}
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                            </svg>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Messages;
