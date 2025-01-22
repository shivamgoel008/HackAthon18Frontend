import React, { useRef, useState } from 'react'
import { useNavigate } from "react-router-dom";
import { checkValidate } from '../Utils/validate';
import Header from './Header'
import Cookies from "js-cookie";
import { login, register } from "../services/loginService";
import {APPLICATION_NAME} from "../Utils/constants"

const Login = () => {
  const navigate = useNavigate();
  const [isSignInForm, setSignInForm] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");

  const toggleSignInForm = () => {
    setSignInForm(!isSignInForm);
  };

  const handleButtonClick = async () => {

    var message = checkValidate(
      email.current?.value,
      password.current?.value,
      name.current?.value,
      isSignInForm
    );

    setErrorMessage(message);

    if (message !== "") return;

    if (isSignInForm) {
      try {
        const data = await login(email.current?.value, password.current?.value)
        console.log(data);
        debugger
        Cookies.set("jwtToken", data.access_token, { secure: true, httpOnly: false });
        navigate("/chat");
      }
      catch (error) {
        console.error('Error making POST request', error);
        setErrorMessage("Try Again With Correct username and password")
      }

    }
    else if (!isSignInForm) {
      // signup logic
      try {
        debugger
        await register(email.current?.value,password.current?.value);
        toggleSignInForm();
        
      } catch (error) {
        setErrorMessage("Please try again after some time");
        console.error('Error making POST request', error);
      }


    }
  }

  const email = useRef(null);
  const password = useRef(null);
  const name = useRef(null);
  return (
    <div className=''>
      <Header />
      <form
        onSubmit={(e) => e.preventDefault()}
        className="w-3/12 absolute p-12  my-48 mx-auto right-0 left-0 rounded-lg bg-opacity-75 text-white"
      >
        <h1 className="font-bold text-black text-3xl py-4">
          {isSignInForm ? "Sign In" : "Sign Up"}
        </h1>

        {!isSignInForm && (
          <input
            ref={name}
            type="text"
            placeholder="Full Name"
            className="p-4 my-4 w-full rounded-lg text-black outline outline-black"
          />
        )}
        <input
          ref={email}
          type="text"
          placeholder="Email Address"
          className="p-4 my-4 w-full outline outline-black rounded-lg text-black"
        />
        <input
          ref={password}
          type="password"
          placeholder="Password"
          className="p-4 my-4 w-full rounded-lg text-black outline outline-black"
        />
        <p className="text-red-500">{errorMessage}</p>
        <button
          className="p-4 my-4  bg-button-green w-full rounded-lg"
          onClick={handleButtonClick}
        >
          {isSignInForm ? "Sign In" : "Sign Up"}
        </button>
        <p className="py-4 cursor-pointer text-black" onClick={toggleSignInForm} >
          {isSignInForm
            ? "New to "+APPLICATION_NAME+ " ? Sign Up Now"
            : "Already registered? Sign In Now"}
        </p>
      </form>
    </div>

  )
}

export default Login