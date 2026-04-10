// --------------------------------------
// API BASE CONFIGURATION
// --------------------------------------

const API_BASE = "http://127.0.0.1:8000";


// --------------------------------------
// TOKEN MANAGEMENT
// --------------------------------------

function saveToken(token) {
    localStorage.setItem("token", token);
}

function getToken() {
    const token = localStorage.getItem("token");

    if (!token || token === "null" || token === "undefined") {
        return null;
    }

    return token;
}

function removeToken() {
    localStorage.removeItem("token");
}


// --------------------------------------
// GENERIC API REQUEST FUNCTION
// --------------------------------------

async function apiRequest(endpoint, method="GET", data=null) {

    const headers = {
        "Content-Type": "application/json"
    };

    const token = getToken();

    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    const options = {
        method: method,
        headers: headers
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    const response = await fetch(API_BASE + endpoint, options);

    let responseData;

    try {
        responseData = await response.json();
    } catch {
        responseData = {};
    }

    if (!response.ok) {
        throw new Error(responseData.detail || "API Error");
    }

    return responseData;
}


// --------------------------------------
// AUTHENTICATION APIs
// --------------------------------------

async function signup(username, email, mobile) {
    return apiRequest("/auth/signup", "POST", {
        username,
        email,
        mobile
    });
}

async function verifyOTP(username, email, mobile, otp, password) {
    return apiRequest("/auth/verify-otp", "POST", {
        username,
        email,
        mobile,
        otp,
        password
    });
}

async function login(email, password) {

    const result = await apiRequest("/auth/login", "POST", {
        email,
        password
    });

    saveToken(result.access_token);

    return result;
}

function logout() {
    removeToken();
    window.location.href = "index.html";
}


// --------------------------------------
// CHAT API
// --------------------------------------

async function sendMessage(message) {
    return apiRequest("/chat", "POST", {
        message: message
    });
}


// --------------------------------------
// ANALYTICS APIs
// --------------------------------------

async function getStats() {
    return apiRequest("/analytics/stats");
}

async function getChatTrend() {
    return apiRequest("/analytics/chat-trend");
}

async function getIntentDistribution() {
    return apiRequest("/analytics/intent-distribution");
}

async function getSentimentDistribution() {
    return apiRequest("/analytics/sentiment-distribution");
}

async function getTopQueries() {
    return apiRequest("/analytics/top-queries");
}

async function getFeedbackStats() {
    return apiRequest("/analytics/feedback-stats");
}


// --------------------------------------
// FEEDBACK API
// --------------------------------------

async function submitFeedback(message, response, rating) {

    return apiRequest("/analytics/feedback", "POST", {
        message,
        response,
        rating
    });
}