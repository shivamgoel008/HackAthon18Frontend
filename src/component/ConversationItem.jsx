import React from 'react'

const ConversationItem = ({time, message,onClick}) => {
    return (
        <div>
            <div className={'conversation-item p-1 dark:bg-gray-700 hover:bg-gray-200 m-1 rounded-md bg-gray-200'} onClick={onClick} >
                <div className={'flex items-center p-2  cursor-pointer  '}>
                    <div className="flex-grow p-2">
                    <div className="text-sm text-gray-500 dark:text-gray-400  w-40 truncate">
                        {message}
                        </div>
                        <div className="flex justify-between text-md "> 
                            <div className="text-xs text-gray-400 dark:text-gray-300">{time}</div>
                        </div>
                        
                    </div>
                </div>
            </div>
        </div>
    )
}

export default ConversationItem
