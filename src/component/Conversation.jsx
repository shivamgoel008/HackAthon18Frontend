import React from 'react';
import ConversationItem from './ConversationItem';

const Conversation = ({ data }) => {
    return (
        <div className="px-1">
            {data.map((item) => (
                <ConversationItem
                    key={item.chatId}
                    message={item.message}
                    time={item.time}
                />
            ))}
        </div>
    );
};

export default Conversation;
