import React from 'react'
import Conversation from './Conversation';
import Messages from './Messages';
import { v4 as uuidv4 } from 'uuid';
import {gptResponse} from '../services/chatService'

const Chat = () => {
    const handleNewChatClick = ()=>{
        const chat_id = uuidv4();
        debugger
        gptResponse(chat_id,"I need help")
    }
    return (
        <div className="">
            <div className="flex bg-white dark:bg-gray-900">
                <div className="w-80 h-screen dark:bg-gray-800 bg-gray-100 p-2 hidden md:block">
                    <div className="h-full overflow-y-auto">
                        <div className="text-xl font-extrabold text-gray-600 dark:text-gray-200 p-3">ChatGpt</div>
                        <div className=' flex justify-between'>
                        <div className="text-lg font-semibol text-gray-600 dark:text-gray-200 p-3">Recent</div>
                        <div className="text-lg font-semibol text-gray-600 dark:text-gray-200 p-3 cursor-pointer" onClick={handleNewChatClick}>New Chat</div>
                        </div>
                        <Conversation/>
                    </div>
                </div>               
                <div className="flex-grow  h-screen p-2 rounded-md">
                        <Messages/>
                </div>
            </div>
        </div>
    )
}

export default Chat
