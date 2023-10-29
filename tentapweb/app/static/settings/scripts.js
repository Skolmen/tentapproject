window.addEventListener('load', function () {
  Notification.requestPermission()
    .then(function (permission) {
      if (permission === 'granted') {
        // The user has granted permission for push notifications
        // You can now subscribe the user to receive push notifications.
      } else if (permission === 'denied') {
        // The user has denied permission for push notifications
      }
    })
    .catch(function (error) {
      console.error('Error while requesting permission:', error);
    });
});

function urlB64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding)
    .replace(/\-/g, '+')
    .replace(/_/g, '/');

  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);

  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}

function registerServiceWorker(serviceWorkerUrl, onRegistrationComplete) {
  var worker = null;

  if ('serviceWorker' in navigator && 'PushManager' in window) {
    console.log('Service Worker and Push are supported');

    navigator.serviceWorker.register(serviceWorkerUrl)
      .then(function (swReg) {
        console.log('Service Worker is registered', swReg);

        // Call the provided callback function to execute custom logic
        if (typeof onRegistrationComplete === 'function') {
          onRegistrationComplete(swReg);
        }

        worker = swReg;
      })
      .catch(function (error) {
        console.error('Service Worker Error', error);
      });
  } else {
    console.warn('Push messaging is not supported');
  }

  return worker;
}

function subscribeUser(serviceWorkerUrl, applicationServerPublicKey) {
  registerServiceWorker(serviceWorkerUrl, function (swReg) {
    const applicationServerKey = urlB64ToUint8Array(applicationServerPublicKey);
    swReg.pushManager.subscribe({
      userVisibleOnly: true,
      applicationServerKey: applicationServerKey
    })
    .then(function(subscription) {
      console.log('User is subscribed.');
  
      return fetch("/api/push-subscriptions", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          subscription_json: JSON.stringify(subscription)
        })
      });
  
    })
    .then(function(response) {
      if (!response.ok) {
        throw new Error('Bad status code from server.');
      }
      return response.json();
    })
    .then(function(responseData) {
      console.log(responseData);
      if (responseData.status!=="success") {
        throw new Error('Bad response from server.');
      }
    })
    .catch(function(err) {
      console.log('Failed to subscribe the user: ', err);
      console.log(err.stack);
    });
  });
}

function unSubscribe(serviceWorkerUrl) {
  registerServiceWorker(serviceWorkerUrl, function (swReg) {
    swReg.pushManager.getSubscription().then((subscription) => {

      if (subscription === null)
        return

      subscription
      .unsubscribe()
      .then((successful) => {
        return fetch("/api/push-unsubscribe", {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            subscription_json: JSON.stringify(subscription)
          })
        });
      })
      .catch((e) => {
        console.log(e)
      });
    });
  });
}

function seeSubscription(serviceWorkerUrl){
  registerServiceWorker(serviceWorkerUrl, function (swReg) {
    swReg.pushManager.getSubscription()
    .then((subscription) => {
      console.log(subscription)
    })
  });

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
