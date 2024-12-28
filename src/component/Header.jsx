import React from 'react'
import logo from '../logo.svg';
const Header = () => {
    return (
        <div className='w-full absolute p-12 py-2 z-10'>
            <img className="w-41" src={logo} alt="logo" />
        </div>
    )
}

export default Header