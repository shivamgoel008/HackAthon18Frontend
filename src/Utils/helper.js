
export function getCookie() {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${"jwtToken"}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}


export function clearCookiesOnLogout() {
    debugger
    const cookies = document.cookie.split(";");

    for (const cookie of cookies) {
        const cookieName = cookie.split("=")[0].trim();
        document.cookie = `${cookieName}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
    }

    console.log("All cookies cleared on logout.");
}

export function getSubjectFromJwt(token) {
    if (!token) return null;

    try {
        const [, payloadBase64] = token.split(".");
        if (!payloadBase64) return null;
        const payload = JSON.parse(atob(payloadBase64));
        return payload.sub || null;
    } catch (error) {
        console.error("Failed to decode JWT token:", error);
        return null;
    }
}

export function getTextBeforeAt(input) {
    if (!input || typeof input !== "string") return null;

    const atIndex = input.indexOf("@");
    if (atIndex === -1) return null; // Return null if '@' is not found

    return input.substring(0, atIndex);
}
