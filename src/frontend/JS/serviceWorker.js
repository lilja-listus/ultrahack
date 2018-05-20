self.addEventListener("install", function(event) {
    // TODO eventually set up caching
});

self.addEventListener("push", function(event) {
    if (event.data) {
        var data = event.data.json();
        
        var title = "Vastoma Overlap Notification"; // TODO localize
        var body;
        if (data.type === "overlap") {
            // TODO localize
            body = data.data.users.join(" and ") + " will overlap in "
                 + data.data.destination + " from " + data.data.start
                 + " to " + data.data.end + "."; // TODO dates human-readable
        }
        event.waitUntil(self.registration.showNotification(title, {
            body: body
        }));
    } else {
        // TODO fail in some useful way?
    }
});
