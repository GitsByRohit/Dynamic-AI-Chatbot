// -------------------------------------
// LOAD DASHBOARD
// -------------------------------------

async function loadDashboard(){

try{

loadStats();
loadChatTrend();
loadIntentDistribution();
loadSentimentDistribution();
loadFeedbackStats();

}catch(err){

console.error("Dashboard error:", err);

}

}


// -------------------------------------
// LOAD BASIC STATS
// -------------------------------------

async function loadStats(){

const data = await getStats();

document.getElementById("totalChats").innerText = data.total_chats;
document.getElementById("activeUsers").innerText = data.active_users;
document.getElementById("fallbackRate").innerText = data.fallback_rate + "%";

}


// -------------------------------------
// CHAT TREND CHART
// -------------------------------------

async function loadChatTrend(){

const data = await getChatTrend();

const labels = data.map(d => d.date);
const values = data.map(d => d.count);

const ctx = document.getElementById("chatTrendChart").getContext("2d");

new Chart(ctx, {

type: "line",

data: {
labels: labels,
datasets: [{
label: "Chats per Day",
data: values,
borderWidth: 2,
fill: false
}]
},

options: {
responsive: true
}

});

}


// -------------------------------------
// INTENT DISTRIBUTION
// -------------------------------------

async function loadIntentDistribution(){

const data = await getIntentDistribution();

const labels = data.map(d => d.intent);
const values = data.map(d => d.count);

const ctx = document.getElementById("intentChart").getContext("2d");

new Chart(ctx, {

type: "pie",

data: {
labels: labels,
datasets: [{
data: values
}]
},

options: {
responsive: true
}

});

}


// -------------------------------------
// SENTIMENT DISTRIBUTION
// -------------------------------------

async function loadSentimentDistribution(){

const data = await getSentimentDistribution();

const labels = data.map(d => d.sentiment);
const values = data.map(d => d.count);

const ctx = document.getElementById("sentimentChart").getContext("2d");

new Chart(ctx, {

type: "pie",

data: {
labels: labels,
datasets: [{
data: values
}]
},

options: {
responsive: true
}

});

}


// -------------------------------------
// FEEDBACK DISTRIBUTION
// -------------------------------------

async function loadFeedbackStats(){

const data = await getFeedbackStats();

const ctx = document.getElementById("feedbackChart").getContext("2d");

new Chart(ctx, {

type: "doughnut",

data: {

labels: ["Helpful", "Not Helpful"],

datasets: [{
data: [data.helpful, data.not_helpful]
}]

},

options: {
responsive: true
}

});

}