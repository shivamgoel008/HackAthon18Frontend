import React, { useEffect, useState } from 'react';
import { formatDistanceToNow } from 'date-fns';
import logo from '../logo.svg';
import { chatHistory, gptResponse } from '../services/chatService';

const Messages = ({ chatId }) => {
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [inputValue, setInputValue] = useState("");
    const [isSending, setIsSending] = useState(false);

    useEffect(() => {
        const fetchMessages = async () => {
            if (!chatId) return;
            setLoading(true);
            setError(null);

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

    const handleSendMessage = async () => {
        if (!inputValue.trim() || isSending) return;
        setIsSending(true);

        try {
            const userMessage = {
                content: inputValue.trim(),
                role: 'user',
                timestamp: new Date().toISOString(),
            };

            // Optimistically add user's message
            setMessages((prevMessages) => [...prevMessages, userMessage]);

            const response = await gptResponse(chatId, inputValue.trim());

            // Add bot response
            setMessages((prevMessages) => [
                ...prevMessages,
                {
                    content: response.message,
                    role: 'bot',
                    timestamp: new Date().toISOString(),
                },
            ]);
            setInputValue("");
        } catch (err) {
            console.error("Error sending message:", err);
            setError("Failed to send message. Please try again.");
        } finally {
            setIsSending(false);
        }
    };

    useEffect(() => {
        // Typing animation logic for the latest bot message
        const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
    
        const animateTyping = async () => {
            const elements = document.getElementsByClassName("typing-animation");
            const lastElement = elements[elements.length - 1]; // Target only the latest bot message
            if (lastElement) {
                const text = lastElement.getAttribute("data-text");
                lastElement.innerHTML = ""; // Clear the content to start typing animation
                for (let character of text) {
                    lastElement.innerHTML += character;
                    await sleep(50); // Adjust typing speed as needed
                }
            }
        };
    
        animateTyping();
    }, [messages]);
    

    if (!chatId) {
        return (
            <div className="text-gray-500 text-center p-5">
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

    return (
        <div className="flex-grow h-full flex flex-col">
            {/* Messages List */}
            <div className="w-full flex-grow bg-gray-100 my-2 p-2 overflow-y-auto">
                {messages.map((item, index) => (
                    item.role === 'user' ? (
                        <div key={index} className="flex justify-end">
                            <div className="flex items-end w-auto m-1 rounded-xl rounded-br-none sm:w-3/4 md:w-auto outline outline-black">
                                <div className="p-2">
                                    <p className="text-black">{item.content}</p>
                                    <div className="flex justify-end text-xs text-gray-400">
                                        {formatDistanceToNow(new Date(item.timestamp), { addSuffix: true })}
                                    </div>
                                </div>
                            </div>
                        </div>
                    ) : (
                        <div key={index} className="flex items-end w-3/4">
                            <img className="w-8 h-8 m-3 rounded-full" src={logo} alt="avatar" />
                            <div className="p-3 mx-3 my-1 rounded-2xl rounded-bl-none sm:w-3/4 md:w-3/6 outline outline-black">
                                <p
                                    className="text-black typing-animation"
                                    data-text={item.content}
                                ></p>
                                <div className="text-xs text-gray-400">
                                    {formatDistanceToNow(new Date(item.timestamp), { addSuffix: true })}
                                </div>
                            </div>
                        </div>
                    )
                ))}
            </div>

            {/* Message Input Section */}
            <div className="h-15 p-3 rounded-xl rounded-tr-none rounded-tl-none bg-gray-100 dark:bg-gray-800">
                <div className="flex items-center">
                    <div className="p-2 text-gray-600 dark:text-gray-200">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                    </div>
                    <div className="search-chat flex flex-grow p-2">
                        <input
                            className="input text-gray-700 dark:text-gray-200 text-sm p-5 focus:outline-none bg-gray-100 dark:bg-gray-800 flex-grow rounded-l-md"
                            type="text"
                            placeholder="Type your message ..."
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                            disabled={isSending}
                        />
                        <div
                            className={`bg-gray-100 dark:bg-gray-800 dark:text-gray-200 flex justify-center items-center pr-3 text-gray-400 rounded-r-md cursor-pointer ${isSending ? 'opacity-50' : ''}`}
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
