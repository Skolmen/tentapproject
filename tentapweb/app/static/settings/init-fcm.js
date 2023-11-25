import { getMessaging, getToken, deleteToken } from "https://www.gstatic.com/firebasejs/10.5.2/firebase-messaging.js"
import { app } from "/static/global/init-firebase.js"
import { queueModal } from "/static/global/modal.js";


// Retrieve Firebase Messaging object.
export const messaging = getMessaging(app);

// Get notifcation status from local storage, if it is not set, set it to false
export function getNotificationStatus() {
    const status = localStorage.getItem("notificationStatus");
    if (status === null) {
        localStorage.setItem("notificationStatus", false);
    }
    return localStorage.getItem("notificationStatus");
}

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
async function subscribeToNotifications(person_id) {
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
                initNotificationSettings();
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
export const callSubscribeToNotifications = (() => {
    let isSubscribing = false;

    return async function(person_id) {
        if (isSubscribing) {
            return;
        }

        isSubscribing = true;

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
        } finally {
            isSubscribing = false;
        }
    }
})();

/**
 * This function unsubscribes from notifications.
 * It first removes the token from the server, then deletes the token on the client.
 * It also updates the local storage settings.
 * @returns {Promise<Object>} A promise that resolves to an object with a status property (boolean) and an optional errorCode property (string).
 */
async function unSubscribeToNotifications() {
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
        resetNotificationSettings();
        return { status: true };
    } catch (err) {
        // If an error occurs, return an object with status: false and errorCode: 'errorUnsubscribingToNotifications'
        return { status: false, errorCode: 'errorUnsubscribingToNotifications' };
    }
}

/**
 * This function calls unSubscribeToNotifications and handles all the output.
 * It displays a loading modal, then calls unSubscribeToNotifications.
 * If the operation is successful, it displays a success modal and logs a success message.
 * If the operation fails, it displays an error modal and logs the error message returned by unSubscribeToNotifications.
 */
export const callUnSubscribeToNotifications = (() => {
    let isUnsubscribing = false;

    return async function() {
        if (isUnsubscribing) {
            return;
        }

        isUnsubscribing = true;

        try {
            queueModal("⏳ Stänger av aviseringar...", "info");
            const result = await unSubscribeToNotifications();
            if (result.status) {
                queueModal("🔕 Aviseringar avslagna!", "success");
                console.log('Token deleted and removed from server.');
            } else {
                let errorMessage;
                switch (result.errorCode) {
                    case 'errorUnsubscribingToNotifications':
                        errorMessage = 'Ett fel uppstod vid avprenumeration på aviseringar.';
                        break;
                    default:
                        errorMessage = 'Ett okänt fel uppstod.';
                }
                queueModal("🚫 " + errorMessage, "error");
                console.log(errorMessage);
            }
        } catch (err) {
            console.log('Error: ', err);
        } finally {
            isUnsubscribing = false;
        }
    }
})();

/**
 * Get the token from local storage.
 * @returns {string} The token from local storage.
 */
function getTokenFromLocalStorage() {
    return localStorage.getItem("token");
}

/**
 * Set the token in local storage.
 * @param {string} token The token to set in local storage.
 */
function setTokenInLocalStorage(token) {
    localStorage.setItem("token", token);
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
export async function detectNewToken() {
    if (localStorage.getItem("token") === null) {
        return;
    }
    let storedToken = getTokenFromLocalStorage();
    let currentToken = await tokenHandler();
    console.log("Current token: " + currentToken + "\nStored token: " + storedToken);
    if (currentToken !== storedToken) {
        try {
            await updateTokenOnServer(storedToken, currentToken);
            setTokenInLocalStorage(currentToken);
            console.log('Token updated on server.');
        } catch (err) {
            console.log('Unable to update token on server. ', err);
            throw err;
        }
    }
    else {
        console.log("Same token");
    }
}

// Export available notification settings
export const availableNotificationSettings = {
    reminderToBook: 'off',
    roomReminderToday: 'off',
    roomReminderTomorrow: 'off'
};

// Get notification settings from local storage
export async function getNotificationSettings() {
    let settings = localStorage.getItem("notificationSettings");
    if (settings === null) {
        settings = availableNotificationSettings;
        localStorage.setItem("notificationSettings", JSON.stringify(settings));
        settings = JSON.stringify(settings);
    }
    return JSON.parse(settings);
}

// Set notification settings in local storage
export function setNotificationSettings(settings) {
    localStorage.setItem("notificationSettings", JSON.stringify(settings));
}

// Initialize notification settings
function initNotificationSettings() {
    getNotificationSettings();
}

// Reset notification settings
function resetNotificationSettings() {
    setNotificationSettings(availableNotificationSettings);
}

export async function updateSettingsForToken(settings) {
    if (localStorage.getItem("notificationStatus") === "false") {
        throw new Error("not-subscribed");
    }
    const currentToken = await tokenHandler();
    await updateSettingsForTokenOnServer(currentToken, settings);
    setNotificationSettings(settings);
}

export function getPersonId() {
    return localStorage.getItem("person_id");
}

async function fetchAPI(endpoint, method, body) {
    const response = await fetch(endpoint, {
        method,
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
    });

    if (!response.ok) {
        throw new Error(`Failed to ${method} ${endpoint}`);
    }

    return response;
}

async function updateTokenOnServer(old_token, new_token) {
    await fetchAPI('/api/updateToken', 'POST', { old_token, new_token });
}

async function sendTokenToServer(token, person_id) {
    await fetchAPI('/api/subscribe', 'POST', { token, person_id });
}

async function removeTokenFromServer(token) {
    await fetchAPI('/api/unsubscribe', 'POST', { token });
}

async function updateSettingsForTokenOnServer(token, settings) {
    await fetchAPI('/api/updateNotificationSettings', 'POST', { token, settings });
}
