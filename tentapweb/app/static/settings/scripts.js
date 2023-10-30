function requestNotificationPermission() {
  return Notification.requestPermission();
}

// Convert a base64 string to a Uint8Array
function urlB64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');
  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);

  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }

  return outputArray;
}

// Promisify service worker registration
function registerServiceWorker(serviceWorkerUrl) {
  if (!('serviceWorker' in navigator && 'PushManager' in window)) {
    console.warn('Push messaging is not supported');
    return Promise.reject('Push messaging is not supported');
  }

  return navigator.serviceWorker.register(serviceWorkerUrl)
    .then(swReg => {
      console.log('Service Worker is registered', swReg);
      return swReg;
    })
    .catch(error => {
      console.error('Service Worker Error', error);
      throw error;
    });
}

// Subscribe user for push notifications
async function subscribeUser(serviceWorkerUrl, applicationServerPublicKey) {
  try {
    const permission = await requestNotificationPermission();

    if (permission === 'granted') {
      const swReg = await registerServiceWorker(serviceWorkerUrl);
      const applicationServerKey = urlB64ToUint8Array(applicationServerPublicKey);
      console.log(swReg)
      const subscription = await swReg.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: applicationServerKey
      });

      console.log('User is subscribed.');
      alert('User is subscribed.');
      await sendSubscriptionToServer(subscription);
    } else if (permission === 'denied') {
      alert("Slå på notiser!")
      // The user has denied permission for push notifications
    }
  } catch (error) {
    console.error('Error while subscribing the user:', error);
  }
}

// Unsubscribe user from push notifications
async function unSubscribe(serviceWorkerUrl) {
  try {
    const swReg = await registerServiceWorker(serviceWorkerUrl);
    const subscription = await swReg.pushManager.getSubscription();

    if (subscription) {
      const successful = await subscription.unsubscribe();
      await sendUnsubscriptionToServer(subscription);
    }
  } catch (error) {
    console.error('Error while unsubscribing the user:', error);
  }
}

// Make the API request to send the subscription to the server
function sendSubscriptionToServer(subscription) {
  return fetch("/api/push-subscriptions", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      subscription_json: JSON.stringify(subscription)
    })
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Bad status code from server.');
    }
    return response.json();
  })
  .then(responseData => {
    console.log(responseData);
    if (responseData.status !== "success") {
      throw new Error('Bad response from server.');
    }
  })
  .catch(err => {
    console.log('Failed to send subscription to the server: ', err);
  });
}

// Make the API request to send the unsubscription to the server
function sendUnsubscriptionToServer(subscription) {
  return fetch("/api/push-unsubscribe", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      subscription_json: JSON.stringify(subscription)
    })
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Bad status code from server.');
    }
    return response.json();
  })
  .then(responseData => {
    if (responseData.status === "unsubscribed") {
      // Handle the "unsubscribed" response
      console.log('User has been successfully unsubscribed.');
    } else {
      throw new Error('Unexpected response from server.');
    }
  })
  .catch(err => {
    console.error('Failed to send unsubscription to the server: ', err);
  });
}

// See the current subscription
async function seeSubscription(serviceWorkerUrl) {
  try {
    const swReg = await registerServiceWorker(serviceWorkerUrl);
    const subscription = await swReg.pushManager.getSubscription();
    console.log(subscription);
  } catch (error) {
    console.error('Error while checking subscription:', error);
  }
}

/*const notificationForm = document.getElementById('notification-form');
notificationForm.addEventListener('submit', function (e) {
    e.preventDefault(); // Prevent the default form submission

    // Get the selected notification status (on or off)
    const selectedStatus = document.querySelector('input[name="notification-status"]:checked').value;

    // Send a POST request to your server
    fetch('/subscribe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: selectedStatus }),
    })
    .then(response => {
        if (response.ok) {
            // Handle a successful response
            console.log('Subscription status updated successfully.');
        } else {
            // Handle an error response
            console.error('Failed to update subscription status.');
        }
    })
    .catch(error => {
        console.error('An error occurred:', error);
    });
});*/
