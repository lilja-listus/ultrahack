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

    function subscribeToPush() {
        navigator.serviceWorker.register("JS/serviceWorker.js")
            .then(function(registration) {
                return registration.pushManager.subscribe({
                    userVisibleOnly: true,
                    applicationServerKey: urlBase64ToUint8Array(
                        "BNIsL4znqW3WbwMBSkZyQQ5Hb3urTmatxOBOgmtEZ03ux6I9LYzCh"
                        + "h6X2-_NSI7HZLeCb8JnHBqTCknQn-i0kws"
                    )
                });
            ).then(function(pushSubscription) {
                callSavePushEndpoint(pushSubscription);
            });
    }


    // Now actually do the stuff
    registerServiceWorker();
    getUserPermission();
    subscribeToPush();

})();
