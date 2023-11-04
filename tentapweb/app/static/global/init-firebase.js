import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.5.2/firebase-app.js'
import firebaseConfig from '../../config/firebase-config';

// Initialize Firebase
export const app = initializeApp(firebaseConfig);

// Wait for the service worker to be ready, then send the Firebase config
navigator.serviceWorker.ready.then(registration => {
    registration.active.postMessage({firebaseConfig});
});