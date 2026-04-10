// -------------------------------------
// LOGIN FORM HANDLER
// -------------------------------------

const loginForm = document.getElementById("loginForm");

if (loginForm) {

loginForm.addEventListener("submit", async function(e){

e.preventDefault();

const email = document.getElementById("email").value;
const password = document.getElementById("password").value;

try {

await login(email, password);

window.location.href = "app.html";

} catch(err){

document.getElementById("errorMessage").innerText = err.message;

}

});

}


// -------------------------------------
// CHECK AUTHENTICATION
// -------------------------------------

function isAuthenticated(){

const token = localStorage.getItem("token");

return token !== null;

}


// -------------------------------------
// PROTECT APP PAGE
// -------------------------------------

function protectPage(){

if(!isAuthenticated()){

window.location.href = "index.html";

}

}


// -------------------------------------
// LOGOUT
// -------------------------------------

function logoutUser(){

localStorage.removeItem("token");

window.location.href = "index.html";

}