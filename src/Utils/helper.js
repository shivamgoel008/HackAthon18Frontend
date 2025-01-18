// utils.js

// Function to get a cookie by name
export function getCookie() {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${"jwtToken"}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}
