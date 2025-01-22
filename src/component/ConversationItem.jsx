import React, { useState } from 'react';
import CustomPopup from './CustomPopup';
import deletebtn from '../delete.svg'

const ConversationItem = ({ time, message, onClick, onDelete }) => {
  const [showPopup, setShowPopup] = useState(false);

  const handleDeleteClick = () => {
    setShowPopup(true);
  };

  const handleConfirm = () => {
    setShowPopup(false);
    onDelete();
  };

  const handleCancel = () => {
    setShowPopup(false);
  };

  return (
    <div>
      <div
        className="conversation-item p-1 bg-[#171717] hover:bg-[#212121] m-1 rounded-md"
        onClick={onClick}
      >
        <div className="flex items-center p-2 cursor-pointer">
          {/* Main Content */}
          <div className="flex-grow p-2">
            <div className="text-sm text-white w-40 truncate">{message}</div>
            <div className="flex justify-between items-center text-md">
              <div className="text-xs text-gray-400 dark:text-gray-300">{time}</div>
            </div>
          </div>

          {/* Delete Button */}
          <button
            onClick={(e) => {
              e.stopPropagation(); // Prevent triggering onClick for the parent
              handleDeleteClick();
            }}
            className="text-red-500 hover:text-red-700 text-xs px-2 py-1 rounded"
          >
            <img src={deletebtn} alt="Delete" className="w-5 h-5 mr-2"/>
            
          </button>
        </div>
      </div>

      {/* Custom Popup */}
      {showPopup && (
        <CustomPopup
          message="Are you sure you want to delete this conversation?"
          onConfirm={handleConfirm}
          onCancel={handleCancel}
        />
      )}
    </div>
  );
};

export default ConversationItem;
