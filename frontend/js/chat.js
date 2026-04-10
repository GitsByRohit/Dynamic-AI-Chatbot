// -------------------------------------
// CHAT UI ELEMENTS
// -------------------------------------

const chatWindow = document.getElementById("chatWindow");
const chatInput = document.getElementById("chatInput");
const sendBtn = document.getElementById("sendBtn");
const newChatBtn = document.getElementById("newChatBtn");
const chatHistoryContainer = document.getElementById("chatHistory");

// conversation id for grouping messages
let conversationId = Date.now();


// -------------------------------------
// SEND MESSAGE EVENT
// -------------------------------------

if (sendBtn) {
    sendBtn.addEventListener("click", sendMessageHandler);
}

if (chatInput) {
    chatInput.addEventListener("keypress", function(e){
        if(e.key === "Enter"){
            sendMessageHandler();
        }
    });
}


// -------------------------------------
// NEW CHAT BUTTON
// -------------------------------------

if(newChatBtn){

    newChatBtn.addEventListener("click", () => {

        chatWindow.innerHTML = "";

        // create new conversation
        conversationId = Date.now();

    });

}


// -------------------------------------
// HANDLE MESSAGE
// -------------------------------------

async function sendMessageHandler(){

    const message = chatInput.value.trim();

    if(message === "") return;

    addUserMessage(message);

    chatInput.value = "";

    addTypingIndicator();

    try{

        const response = await fetch("http://127.0.0.1:8000/chat",{

            method:"POST",

            headers:{
                "Content-Type":"application/json",
                "Authorization":"Bearer " + localStorage.getItem("token")
            },

            body:JSON.stringify({
                message: message,
                conversation_id: conversationId
            })

        });

        const data = await response.json();

        removeTypingIndicator();

        addBotMessage(data.response);

        loadChatHistory();

    }catch(err){

        removeTypingIndicator();

        addBotMessage("Error: Unable to reach server.");

    }

}


// -------------------------------------
// USER MESSAGE BUBBLE
// -------------------------------------

function addUserMessage(text){

    const wrap = document.createElement("div");
    wrap.classList.add("bubble-wrap","user");

    const avatar = document.createElement("div");
    avatar.classList.add("avatar");
    avatar.innerText = "👤";

    const bubble = document.createElement("div");
    bubble.classList.add("bubble-text");
    bubble.innerText = text;

    wrap.appendChild(avatar);
    wrap.appendChild(bubble);

    chatWindow.appendChild(wrap);

    scrollToBottom();

}


// -------------------------------------
// BOT MESSAGE BUBBLE
// -------------------------------------

function addBotMessage(text){

    const wrap = document.createElement("div");
    wrap.classList.add("bubble-wrap","bot");

    const avatar = document.createElement("div");
    avatar.classList.add("avatar");
    avatar.innerText = "🤖";

    const bubble = document.createElement("div");
    bubble.classList.add("bubble-text");
    bubble.innerText = text;

    // feedback container
    const feedbackDiv = document.createElement("div");
    feedbackDiv.classList.add("feedback-container");

    const likeBtn = document.createElement("button");
    likeBtn.innerText = "👍";

    const dislikeBtn = document.createElement("button");
    dislikeBtn.innerText = "👎";

    likeBtn.onclick = () => sendFeedback(1);
    dislikeBtn.onclick = () => sendFeedback(-1);

    feedbackDiv.appendChild(likeBtn);
    feedbackDiv.appendChild(dislikeBtn);

    bubble.appendChild(feedbackDiv);

    wrap.appendChild(avatar);
    wrap.appendChild(bubble);

    chatWindow.appendChild(wrap);

    scrollToBottom();

}


// -------------------------------------
// SEND FEEDBACK
// -------------------------------------

async function sendFeedback(rating){

    try{

        await fetch("http://127.0.0.1:8000/analytics/feedback",{

            method:"POST",

            headers:{
                "Content-Type":"application/json",
                "Authorization":"Bearer " + localStorage.getItem("token")
            },

            body:JSON.stringify({
                rating:rating
            })

        });

    }catch(err){

        console.error("Feedback failed");

    }

}


// -------------------------------------
// TYPING INDICATOR
// -------------------------------------

let typingDiv = null;

function addTypingIndicator(){

    typingDiv = document.createElement("div");
    typingDiv.classList.add("bubble-wrap","bot");

    const bubble = document.createElement("div");
    bubble.classList.add("bubble-text");
    bubble.innerText = "AI is typing...";

    typingDiv.appendChild(bubble);

    chatWindow.appendChild(typingDiv);

    scrollToBottom();

}

function removeTypingIndicator(){

    if(typingDiv){
        chatWindow.removeChild(typingDiv);
        typingDiv = null;
    }

}


// -------------------------------------
// SCROLL CHAT WINDOW
// -------------------------------------

function scrollToBottom(){

    chatWindow.scrollTop = chatWindow.scrollHeight;

}


// -------------------------------------
// LOAD CHAT HISTORY (SIDEBAR)
// -------------------------------------

async function loadChatHistory(){

    try{

        const response = await fetch("http://127.0.0.1:8000/chat/history",{

            headers:{
                "Authorization":"Bearer " + localStorage.getItem("token")
            }

        });

        const data = await response.json();

        if(!chatHistoryContainer) return;

        chatHistoryContainer.innerHTML = "";

        data.forEach(chat => {

            const item = document.createElement("div");

            item.classList.add("recent-item");

            item.innerText = chat.title;

            item.onclick = () => loadConversation(chat.conversation_id);

            chatHistoryContainer.appendChild(item);

        });

    }catch(err){

        console.log("Unable to load history");

    }

}


// -------------------------------------
// LOAD OLD CONVERSATION
// -------------------------------------

async function loadConversation(chatId){

    try{

        // IMPORTANT FIX
        conversationId = chatId;

        const response = await fetch(`http://127.0.0.1:8000/chat/history/${chatId}`,{

            headers:{
                "Authorization":"Bearer " + localStorage.getItem("token")
            }

        });

        const messages = await response.json();

        chatWindow.innerHTML = "";

        messages.forEach(msg => {

            addUserMessage(msg.message);
            addBotMessage(msg.response);

        });

    }catch(err){

        console.log("Failed to load conversation");

    }

}


// -------------------------------------
// LOAD PROFILE EMAIL
// -------------------------------------

window.addEventListener("load", () => {

    const email = localStorage.getItem("signup_email");
    const profileEmail = document.getElementById("profileEmail");

    if(profileEmail && email){

        const username = email.split("@")[0];

        profileEmail.innerText = "User: " + username;

    }

    loadChatHistory();

});