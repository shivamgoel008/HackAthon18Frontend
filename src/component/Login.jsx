import React, { useRef, useState } from 'react'
import { useDispatch } from 'react-redux';
import { useNavigate } from "react-router-dom";
import { checkValidate } from '../Utils/validate';
import axios from 'axios';
import Header from './Header'
import { addUser } from '../Utils/userSlice';
import Cookies from "js-cookie";


const Login = () => {
  const dispatch = useDispatch();
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

    const payload = {
      username: email.current?.value,
      password: password.current?.value,
    };
    setErrorMessage(message);

    if (message !== "") return;

    if (isSignInForm) {
      try {
        const response = await axios.post("http://127.0.0.1:5000/login", payload);
        console.log(response);
        debugger
        if (response.status===200) {

          Cookies.set("jwtToken", response.data.access_token, { secure: true, httpOnly: false });

        navigate("/chat");
          navigate("/chat");
        }
      } catch (error) {
        console.error('Error making POST request', error);
        setErrorMessage("Try Again With Correct username and password")
      }

    }
    else if (!isSignInForm) {
      // signup logic
      try {
        debugger
        const response = await axios.post("http://127.0.0.1:5000/register", payload);
        if (response.status === 200) {
          toggleSignInForm();
        }
      } catch (error) {
        console.error('Error making POST request', error);
      }


    }
  }

  const email = useRef(null);
  const password = useRef(null);
  const name = useRef(null);
  return (
    <div className=' bg-black  bg-opacity-50'>
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
            ? "New to ChatGPT? Sign Up Now"
            : "Already registered? Sign In Now"}
        </p>
      </form>
    </div>

  )
}

export default Login