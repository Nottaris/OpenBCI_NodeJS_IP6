looking = false;
window.onload = function () {
    var tracker = new tracking.ObjectTracker('face');
    tracker.setInitialScale(1);
    tracker.setStepSize(2);
    tracker.setEdgesDensity(0.1);
    tracking.track('#video', tracker, {camera: true});
    tracker.on('track', function (event) {
        looking = false;
        event.data.forEach(function () {
            looking = true;
        });
    });
};