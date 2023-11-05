import { getMessaging, getToken, deleteToken } from "https://www.gstatic.com/firebasejs/10.5.2/firebase-messaging.js"
import { app } from "/static/global/init-firebase.js"
import { queueModal } from "/static/global/modal.js";


// Retrieve Firebase Messaging object.
export const messaging = getMessaging(app);

/**
 * Retrieves the current token.
 *
 * This function calls the `getToken` function from Firebase Cloud Messaging (FCM) with the messaging service and the public VAPID key.
 * It returns the current token if one exists, or generates a new one if it doesn't.
 *
 * @function tokenHandler
 * @returns {Promise<string>} The current token or a new token.
 */
export function tokenHandler() {
    return getToken(messaging, { vapidKey: VAPID_PUBLIC_KEY });
}

/**
 * Subscribes to notifications for a specific person.
 *
 * This function first requests notification permission from the user.
 * If permission is granted, it retrieves the current token by calling the `tokenHandler` function.
 * If a token is retrieved, it sends the token and the person_id to the server by calling the `sendTokenToServer` function.
 * If the token is successfully sent, it displays a success message, sets the "notificationStatus", "person_id", and "token" in local storage,
 * and logs "Token sent to server." to the console.
 * If unable to send the token, it logs an error to the console.
 * If no token is retrieved, it logs "No registration token available. Request permission to generate one." to the console.
 * If unable to retrieve a token, it displays an error message and logs an error to the console.
 * If permission is not granted, it logs "Unable to get permission to notify." to the console.
 *
 * @function subscribeToNotifications
 * @param {string} person_id - The ID of the person to subscribe to notifications for.
 * @throws Will log an error to the console if unable to get permission, retrieve the token, or send the token to the server.
 */
export function subscribeToNotifications(person_id) {
    queueModal("⏳ Slår på aviseringar...", "info");
    Notification.requestPermission().then((permission) => {
        if (permission === 'granted') {
            console.log('Notification permission granted.');
            // Add the public key generated from the console here.
            tokenHandler().then((currentToken) => {
                if (currentToken) {
                    console.log(currentToken);
                    sendTokenToServer(currentToken, person_id).then(() => {
                        queueModal("🔔 Aviseringar påslagna!", "success");
                        localStorage.setItem("notificationStatus", true);
                        localStorage.setItem("person_id", person_id);
                        localStorage.setItem("token", currentToken);
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

/**
 * Detects if the token has changed and updates it on the server if it has.
 * 
 * This function first checks if the notification status is set to false in local storage.
 * If it is, the function returns immediately. If not, it retrieves the stored token from local storage.
 * It then gets the current token by calling the `tokenHandler` function.
 * If the current token is different from the stored token, it calls the `updateTokenOnServer` function
 * to update the token on the server and then updates the token in local storage.
 * If the current token is the same as the stored token, it logs "Same token" to the console.
 *
 * @function detectNewToken
 * @throws Will log an error to the console if unable to update the token on the server.
 */
export function detectNewToken() {
    return new Promise((resolve, reject) => {
        if (localStorage.getItem("notificationStatus") === "false") {
            resolve();
            return;
        }
        let storedToken = localStorage.getItem("token");
        tokenHandler().then((currentToken) => {
            console.log("Current token: " + currentToken + "\nStored token: " + storedToken);
            if (currentToken !== storedToken) {
                updateTokenOnServer(storedToken, currentToken).then(() => {
                    localStorage.setItem("token", currentToken);
                    console.log('Token updated on server.');
                    resolve();
                }).catch((err) => {
                    console.log('Unable to update token on server. ', err);
                    reject(err);
                });
            }
            else {
                console.log("Same token");
                resolve();
            }
        });
    });
}

/**
 * Unsubscribes from notifications.
 * 
 * This function first retrieves the current token by calling the `tokenHandler` function.
 * It then calls the `deleteToken` function to delete the token from the messaging service.
 * If the token is successfully deleted, it calls the `removeTokenFromServer` function to remove the token from the server.
 * If the token is successfully removed from the server, it displays a success message, sets the "notificationStatus" in local storage to false,
 * and removes the "token" and "person_id" from local storage.
 * If any of these operations fail, it logs an error to the console.
 *
 * @function unSubscribeToNotifications
 * @throws Will log an error to the console if unable to get the token, delete the token, or remove the token from the server.
 */
export async function unSubscribeToNotifications() {
    try {
        queueModal("⏳ Stänger av aviseringar...", "info");
        await detectNewToken();
        const token = await tokenHandler();
        // Remove token from server first
        await removeTokenFromServer(token);
        console.log('Token removed from server.');
        // Then delete token on the client
        await deleteToken(messaging, token);
        console.log('Token deleted.');
        queueModal("🔕 Aviseringar avslagna!", "success");
        localStorage.setItem("notificationStatus", false);
        localStorage.removeItem("token");
        localStorage.removeItem("person_id");
        setLocalStorageSettings(false);
    } catch (err) {
        queueModal("🚫 Ett fel inträffade! Försök igen.", "error")
        console.log('Error: ', err);
    }
}

export function updateSettingsForToken() {
    return new Promise((resolve, reject) => {
        if (localStorage.getItem("notificationStatus") === "false") {
            reject("not-subscribed");
            return;
        }
        tokenHandler().then((currentToken) => {
            const form = document.getElementById("notificaiton-settings");
            const formData = new FormData(form);
            const settings = {};
            for (const pair of formData.entries()) {
                settings[pair[0]] = pair[1];
            }
            console.log(settings);
            updateSettingsForTokenOnServer(currentToken, settings).then(() => {
                resolve();
            }).catch((err) => {
                reject(err);
            });
        }
        );
    }
    );
}

export function setLocalStorageSettings(bool) {
    localStorage.setItem("reminder", bool);
    localStorage.setItem("roomReminder", bool);
    localStorage.setItem("roomReminderTomorrow", bool);
}

/**
 * Updates the token on the server.
 *
 * @async
 * @function updateTokenOnServer
 * @param {string} old_token - The old token to be replaced.
 * @param {string} new_token - The new token to replace the old one.
 * @throws Will throw an error if the response from the server is not ok.
 */
async function updateTokenOnServer(old_token, new_token) {
    const response = await fetch('/api/updateToken', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ old_token, new_token }),
    });

    if (!response.ok) {
        throw new Error('Failed to update token on server');
    }
}

/**
 * Sends the token and person_id to the server.
 *
 * @async
 * @function sendTokenToServer
 * @param {string} token - The token to be sent.
 * @param {string} person_id - The person_id to be sent.
 * @throws Will throw an error if the response from the server is not ok.
 */
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

/**
 * Removes the token from the server.
 *
 * @async
 * @function removeTokenFromServer
 * @param {string} token - The token to be removed.
 * @throws Will throw an error if the response from the server is not ok.
 */
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

async function updateSettingsForTokenOnServer(token, settings) {
    const response = await fetch('/api/updateNotificationSettings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token, settings }),
    });

    if (!response.ok) {
        throw new Error('Failed to update settings for token on server');
    }
}
