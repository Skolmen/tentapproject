import { onMessage } from "https://www.gstatic.com/firebasejs/10.5.2/firebase-messaging.js"
import { messaging } from "/static/settings/init-fcm.js"

//Listen for messages
/*onMessage(messaging, (payload) => {
    console.log('Message received. ', payload);
    // ...
});*/