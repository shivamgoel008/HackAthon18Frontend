import React from 'react';
import debuggers from '../debugger.png'
import {WELCOME_TEXT} from '../Utils/constants'
import { useLocation } from 'react-router-dom'; 
import { clearCookiesOnLogout, getCookie, getSubjectFromJwt, getTextBeforeAt } from '../Utils/helper';

const Header = () => {
  const location = useLocation(); 
  const username = getTextBeforeAt(getSubjectFromJwt(getCookie())); 

  const handleLogout = () => {
    debugger
    clearCookiesOnLogout()
    window.location.href = '/'; 
  };

  // Check if the current path is the login page
  const isLoginPage = location.pathname === '/'; 

  return (
    <div className='w-full relative p-12 py-2 z-10 flex justify-between'> 
      <img className="w-15 h-10" src={debuggers} alt="logo" />

      { !isLoginPage && ( 
        <>
          {username && (
            <span className="text-gray-700 font-semibold mr-4 mt-3"> 
             {WELCOME_TEXT} {username}
            </span>
          )} 
          <button 
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" 
            onClick={handleLogout} 
          >
            Logout
          </button>
        </>
      )}
    </div>
  );
};

export default Header;