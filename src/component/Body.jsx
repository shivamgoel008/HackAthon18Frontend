import React from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Login from "./Login";
import Header from "./Header";

const Body = () => {
    const appRouter = createBrowserRouter([
        {
            path: "/",
            element: <Login />
        },
        {
            path: "/header",
            element: <Header />
        }
    ])
    return (
        <div>
            <RouterProvider router={appRouter}/>
        </div>
    );
};

export default Body;
