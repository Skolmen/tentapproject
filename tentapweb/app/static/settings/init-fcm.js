import { getMessaging, getToken, deleteToken, onMessage } from "https://www.gstatic.com/firebasejs/10.5.2/firebase-messaging.js"
import { app } from "/static/global/init-firebase.js"
import { queueModal } from "/static/global/modal.js";



// Retrieve Firebase Messaging object.
export const messaging = getMessaging(app);

//Token retrieval function
export function tokenHandler() {
    return getToken(messaging, { vapidKey: VAPID_PUBLIC_KEY });
}

//Request permission to send notifications
export function subscribeToNotifications(person_id) {
    Notification.requestPermission().then((permission) => {
        if (permission === 'granted') {
            console.log('Notification permission granted.');
            // Add the public key generated from the console here.
            tokenHandler().then((currentToken) => {
                if (currentToken) {
                    // Send the token to your server and update the UI if necessary
                    // ...
                    console.log(currentToken);
                    sendTokenToServer(currentToken, person_id).then(() => {
                        queueModal("🔔 Aviseringar påslagna!", "success");
                        localStorage.setItem("notificationStatus", true);
                        localStorage.setItem("person_id", person_id);
                        console.log('Token sent to server.');
                    }
                    ).catch((err) => {
                        console.log('Unable to send token to server. ', err);
                    });
                } else {
                    // Show permission request UI
                    console.log('No registration token available. Request permission to generate one.');
                    // ...
                }
            }).catch((err) => {
                queueModal("🚫 Ett fel inträffade! Försök igen.", "error");
                console.log('An error occurred while retrieving token. ', err);
                // ...
            });
        } else {
            console.log('Unable to get permission to notify.');
        }
    });
}


// Function to send token to server
async function sendTokenToServer(token, person_id) {
    const response = await fetch('/api/subscribe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token, person_id }),
    });

    if (!response.ok) {
        throw new Error('Bad status code from server.');
    }
}

// Function to remove token from server
async function removeTokenFromServer(token) {
    const response = await fetch('/api/unsubscribe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token }),
    });

    if (!response.ok) {
        throw new Error('Failed to remove token from server');
    }
}

// Unsubscribe from notifications function
export function unSubscribeToNotifications() {
    tokenHandler().then((token) => {
        deleteToken(messaging).then(() => {
            console.log('Token deleted.');
            // Remove token from server
            removeTokenFromServer(token).then(() => {
                queueModal("🔕 Aviseringar avslagna!", "success");
                localStorage.setItem("notificationStatus", false);
                localStorage.removeItem("person_id");
                console.log('Token removed from server.');
            }).catch((err) => {
                console.log('Unable to remove token from server. ', err);
            });
        }).catch((err) => {
            console.log('Unable to delete token. ', err);
        });
    }).catch((err) => {
        console.log('Unable to get token. ', err);
    });
}

