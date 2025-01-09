import React from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Login from "./Login";
import Chat from "./Chat";

const Body = () => {
    const appRouter = createBrowserRouter([
        {
            path: "/",
            element: <Login />
        },
        {
            path: "/chat",
            element: <Chat />
        }
    ])
    return (
        <div>
            <RouterProvider router={appRouter}/>
        </div>
    );
};

export default Body;
