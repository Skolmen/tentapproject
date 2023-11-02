import { getMessaging, getToken } from "https://www.gstatic.com/firebasejs/10.5.2/firebase-messaging.js"
import { app } from "/static/settings/init-firebase.js"

export const messaging = getMessaging();

export function requestPermission() {
  console.log('Requesting permission...');
  Notification.requestPermission().then((permission) => {
    if (permission === 'granted') {
      console.log('Notification permission granted.');

      if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/firebase-messaging-sw.js')
          .then(function (registration) {
            console.log('Registration successful, scope is:', registration.scope);
            navigator.serviceWorker.ready.then(() => {
              getToken(messaging, { serviceWorkerRegistration: registration, vapidKey: VAPID_PUBLIC_KEY })
                .then((currentToken) => {
                  if (currentToken) {
                    console.log(currentToken)
                    showModal("Aviersingar påslagna!", "green")
                    // Send the token to your server and update the UI if necessary
                    // ...
                  } 
                }).catch((err) => {
                  showModal("Ett fel inträffade vid uppstart av aviseringar!", "red")
                  console.log('An error occurred while retrieving token. ', err);
                });
            });
          }).catch(function (err) {
            console.log('Service worker registration failed, error:', err);
          });
      }
      else {
        showModal("Din webbläsare stödjer inte aviseringar!", "red")
      }
    }
    else {
      showModal("Du måste tillåta aviseringar!", "red")
    }
  });
}


export function unSubscribe() {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.getRegistration('/firebase-messaging-sw.js').then((registration) => {
        if (registration) {
          getToken(messaging, { serviceWorkerRegistration: registration, vapidKey: VAPID_PUBLIC_KEY })
          .then((currentToken) => {
            if (currentToken) {
              console.log(currentToken)
              //Remove token from server
              // ...
            } 
          }).catch((err) => {
            showModal("Ett fel inträffade vid avstängning av aviseringar!", "red")
            console.log('An error occurred while disabling notification. ', err);
          });
          console.log("gd")
          registration.unregister();   
        }
     
    });
  }
  showModal("Aviseringar avstängda!", "green");
  localStorage.setItem("notificationStatus", false);
  console.log("Unsubscribed");
}


