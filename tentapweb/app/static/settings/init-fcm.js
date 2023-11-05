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
 * This function subscribes to notifications for a specific person.
 * It first requests notification permission from the user.
 * If permission is granted, it retrieves the current token by calling the `tokenHandler` function.
 * If a token is retrieved, it sends the token and the person_id to the server by calling the `sendTokenToServer` function.
 * It also updates the local storage settings.
 * @param {string} person_id - The ID of the person to subscribe to notifications for.
 * @returns {Promise<Object>} A promise that resolves to an object with a status property (boolean) and an optional errorCode property (string).
 */
export async function subscribeToNotifications(person_id) {
    try {
        const permission = await Notification.requestPermission();
        if (permission === 'granted') {
            console.log('Notification permission granted.');
            const currentToken = await tokenHandler();
            if (currentToken) {
                console.log(currentToken);
                await sendTokenToServer(currentToken, person_id);
                localStorage.setItem("notificationStatus", true);
                localStorage.setItem("person_id", person_id);
                localStorage.setItem("token", currentToken);
                // If everything is successful, return an object with status: true
                return { status: true };
            } else {
                console.log('No registration token available. Request permission to generate one.');
                // If no token is available, return an object with status: false and errorCode: 'noTokenAvailable'
                return { status: false, errorCode: 'noTokenAvailable' };
            }
        } else {
            console.log('Unable to get permission to notify.');
            // If unable to get permission, return an object with status: false and errorCode: 'unableToGetPermission'
            return { status: false, errorCode: 'unableToGetPermission' };
        }
    } catch (err) {
        // If an error occurs, return an object with status: false and errorCode: 'errorSubscribingToNotifications'
        return { status: false, errorCode: 'errorSubscribingToNotifications' };
    }
}

/**
 * This function calls subscribeToNotifications and handles all the output.
 * It displays a loading modal, then calls subscribeToNotifications.
 * If the operation is successful, it displays a success modal and logs a success message.
 * If the operation fails, it displays an error modal and logs an error message.
 * @param {string} person_id - The ID of the person to subscribe to notifications for.
 */
export async function callSubscribeToNotifications(person_id) {
    try {
        queueModal("⏳ Slår på aviseringar...", "info");
        const result = await subscribeToNotifications(person_id);
        if (result.status) {
            queueModal("🔔 Aviseringar påslagna!", "success");
            console.log('Token sent to server.');
        } else {
            let errorMessage;
            switch (result.errorCode) {
                case 'noTokenAvailable':
                    errorMessage = 'Kunde inte generara en token.';
                    break;
                case 'unableToGetPermission':
                    errorMessage = 'Du måste tillåta aviseringer.';
                    break;
                case 'errorSubscribingToNotifications':
                    errorMessage = 'Ett fel uppstod vid prenumeration på aviseringar.';
                    break;
                default:
                    errorMessage = 'Ett okänt fel uppstod.';
            }
            queueModal("🚫 " + errorMessage, "error");
            console.log(errorMessage);
        }
    } catch (err) {
        console.log('Error: ', err);
    }
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
 * This function unsubscribes from notifications.
 * It first removes the token from the server, then deletes the token on the client.
 * It also updates the local storage settings.
 * @returns {Promise<boolean>} A promise that resolves to a boolean value indicating the success or failure of the operation.
 */
export async function unSubscribeToNotifications() {
    try {
        await detectNewToken();
        const token = await tokenHandler();
        // Remove token from server first
        await removeTokenFromServer(token);
        // Then delete token on the client
        await deleteToken(messaging, token);
        localStorage.setItem("notificationStatus", false);
        localStorage.removeItem("token");
        localStorage.removeItem("person_id");
        setLocalStorageSettings(false);
        return true;
    } catch (err) {
        return false;
    }
}

/**
 * This function calls unSubscribeToNotifications and handles all the output.
 * It displays a loading modal, then calls unSubscribeToNotifications.
 * If the operation is successful, it displays a success modal and logs a success message.
 * If the operation fails, it displays an error modal and logs an error message.
 */
export async function callUnSubscribeToNotifications() {
    try {
        queueModal("⏳ Stänger av aviseringar...", "info");
        const result = await unSubscribeToNotifications();
        if (result) {
            queueModal("🔕 Aviseringar avslagna!", "success");
            console.log('Token deleted and removed from server.');
        } else {
            queueModal("🚫 Ett fel inträffade! Försök igen.", "error");
            console.log('Error occurred while unsubscribing to notifications.');
        }
    } catch (err) {
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
