// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import 'firebase/auth';

const firebaseConfig = {
  apiKey: "AIzaSyCYnMU1Qwv_94uHWXupTd1GXtRAvG5tntc",
  authDomain: "authtrail-9db60.firebaseapp.com",
  projectId: "authtrail-9db60",
  storageBucket: "authtrail-9db60.appspot.com",
  messagingSenderId: "788177298866",
  appId: "1:788177298866:web:a8d1f2ce0afc5376f370ab",
  measurementId: "G-BQFZD7JP44"
};


// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);


// Get a reference to the Firebase Authentication service
const auth = firebase.auth();

// Get a reference to the HTML elements for the email and password input fields
var emailInput = document.getElementById('email-input');
var passwordInput = document.getElementById('password-input');

// Add an event listener to the form submit button
var submitButton = document.getElementById('submit-button');
submitButton.addEventListener('click', function(event) {
  event.preventDefault(); // prevent the default form submission

  // Get the email and password entered by the user
  var email = emailInput.value;
  var password = passwordInput.value;

  // Create a new user account with the email and password
  auth.createUserWithEmailAndPassword(email, password)
    .then(function(userCredential) {
      // Generate a permission code and display it to the user
      var permissionCode = generatePermissionCode();
      alert('Your permission code is: ' + permissionCode);
    })
    .catch(function(error) {
      // Handle any errors that occur during account creation
      alert('An error occurred: ' + error.message);
    });
});

function generatePermissionCode() {
  const randomCode = Math.floor(Math.random() * 900000) + 100000;
}