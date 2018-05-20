(function () {

    // Code closely follows that of 
    // https://developers.google.com/web/fundamentals/push-notifications

    if (!("serviceWorker" in navigator) || !("PushManager" in window)) {
        return; // TODO can't use push notification in this browser
    }

    function registerServiceWorker() {
        return navigator.serviceWorker.register("JS/serviceWorker.js")
            .then(function(registration) {
                return registration; // Success!
            }).catch(function(err) {
                console.error("Service worker registration failed.", err);
            });
    }

    function getUserPermission() {
        return new Promise(function(resolve, reject) {
            const permission = Notification.requestPermission(function(result) {
                resolve(result);
            });

            if (permission) {
                permission.then(resolve, reject);
            }
        }).then(function(permission) {
            if (permission !== "granted") {
                throw new Error("Permission not granted.");
            }
        });
    }

    function callSavePushEndpoint(subscription) {
        return fetch("api/save_push_subscription", {
            method: "POST",
            headers: {
                "Content-Type" : "application/json"
            },
            body: JSON.stringify(subscription)
        }).then(function(response) {
            if (!response.ok) { throw new Error("callSavePushEndpoint 1"); }
            return response.json();
        }).then(function(responseData) {
            // XXX Nothing in particular to do here
        });
    
    }


    // From https://github.com/GoogleChromeLabs/web-push-codelab/blob/master/app/scripts/main.js,
    // which appears to be under apache license.
    // Was originally called urlB64ToUint8Array
    function urlBase64ToUint8Array(base64String) {
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

    function subscribeToPush() {
        navigator.serviceWorker.register("JS/serviceWorker.js")
            .then(function(registration) {
                return registration.pushManager.subscribe({
                    userVisibleOnly: true,
                    applicationServerKey: urlBase64ToUint8Array(
                    "BOs0jAT7TZgCoSlCfOUhFTzOFq339unvnkbQFd_atBMjOm9o4T7OKiEerFn" 
                    + "goPEAtEsgVw219s5E5BnL9P2IvtI"
                    )
                });
            }).then(function(pushSubscription) {
                callSavePushEndpoint(pushSubscription);
            });
    }


    // Now actually do the stuff
    registerServiceWorker();
    getUserPermission();
    subscribeToPush();

})();
