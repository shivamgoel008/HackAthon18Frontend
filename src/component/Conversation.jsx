import React from 'react';
import ConversationItem from './ConversationItem';

const Conversation = ({ data,onClick }) => {
    return (
        <div className="px-1">
            {data.map((item) => (
                <ConversationItem
                    key={item.chatId}
                    message={item.message}
                    time={item.time}
                    onClick={() => onClick(item.chatId)}
                />
            ))}
        </div>
    );
};

export default Conversation;
