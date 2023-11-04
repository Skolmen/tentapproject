importScripts('https://www.gstatic.com/firebasejs/9.2.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/9.2.0/firebase-messaging-compat.js');

let firebaseConfig;

// Listen for the message event to receive the Firebase config
self.addEventListener('message', event => {
  if (event.data && event.data.firebaseConfig) {
    firebaseConfig = event.data.firebaseConfig;

    // Initialize Firebase with the received configuration
    firebase.initializeApp(firebaseConfig);
    const messaging = firebase.messaging();

    messaging.onBackgroundMessage(function(payload) {
      console.log('[firebase-messaging-sw.js] Received background message ', payload);
      // Customize notification here
    });
  }
});