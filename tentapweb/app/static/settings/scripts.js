//NOTE!!!!
//THIS FILE IS NOT IN USE, LEAVE IT BE FOR NOW

import { getMessaging, getToken, deleteToken } from "https://www.gstatic.com/firebasejs/10.5.2/firebase-messaging.js"
import { app } from "/static/settings/init-firebase.js"
import { hejFromBookingScript } from "/static/booking/scripts.js";

export const messaging = getMessaging();

function handleServiceWorkerRegistration(path) {
  if ('serviceWorker' in navigator) {
    return navigator.serviceWorker.register(path);
  } else {
    showModal("Din webbläsare stödjer inte aviseringar!", "red");
    return Promise.reject(new Error('Service worker not supported'));
  }
}

function handleTokenRetrieval(messaging, options) {
  return getToken(messaging, options)
    .then((currentToken) => {
      if (currentToken) {
        console.log(currentToken);
        return currentToken;
      } else {
        throw new Error('No token available');
      }
    });
}


export function subscribeToNotifications(person_id) {
  hejFromBookingScript();
  console.log('Requesting permission...');
  Notification.requestPermission().then((permission) => {
    if (permission === 'granted') {
      console.log('Notification permission granted.');
      handleServiceWorkerRegistration('/firebase-messaging-sw.js')
        .then((registration) => {
          if (registration) {
            navigator.serviceWorker.ready.then(() => {
              handleTokenRetrieval(messaging, { serviceWorkerRegistration: registration, vapidKey: VAPID_PUBLIC_KEY })
                .then((token) => {
                  // Send the token to the server with the person_id
                  // You need to implement this function
                  // sendTokenToServer(token, person_id);

                  showModal("Aviseringar påslagna!", "green");
                  localStorage.setItem("notificationStatus", true);
                }).catch((err) => {
                  showModal("Ett fel inträffade vid uppstart av aviseringar!", "red");
                  console.log('An error occurred while retrieving token. ', err);
                });
            });
          }
        });
    } else {
      showModal("Du måste tillåta aviseringar!", "red");
    }
  });
}

export function unSubscribeToNotifications() {
  deleteToken(messaging);
  if (Notification.permission === 'granted') {
    console.log('Notifications are granted. Unsubscribing...');
    navigator.serviceWorker.getRegistration('/firebase-messaging-sw.js')
      .then((registration) => {
        if (registration) {
          handleTokenRetrieval(messaging, { serviceWorkerRegistration: registration, vapidKey: VAPID_PUBLIC_KEY })
            .then((token) => {
              // Delete the token from the server
              // Placeholder for your implementation
              // deleteTokenFromServer(token);

              registration.unregister();
              showModal("Aviseringar avstängda!", "green");
              localStorage.setItem("notificationStatus", false);
              console.log("Unsubscribed");
            }).catch((err) => {
              showModal("Ett fel inträffade vid avstängning av aviseringar!", "red")
              console.log('An error occurred while disabling notification. ', err);
            });
        } else {
          console.log('Service worker not found. No need to unsubscribe.');
        }
      });
  } else {
    console.log('Notifications are not granted. No need to unsubscribe.');
  }
}
