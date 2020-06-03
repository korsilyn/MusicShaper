/// <reference path="../../libs/@types/paper.d.ts" />

/** @type {paper.Project} */
var project;

var scrollValue = 0;

project.view.element.addEventListener('wheel', function (event) {
    var oldScrollValue = scrollValue;
    scrollValue += event.deltaY;
    if (scrollValue < 0) {
        scrollValue = 0;
    }

    project.view.scrollBy(scrollValue - oldScrollValue, 0);

    if (oldScrollValue == 0 && scrollValue != 0) {
        window.dispatchEvent(new window.Event('timelineScrollAway'));
    }
    else if (oldScrollValue != 0 && scrollValue == 0) {
        window.dispatchEvent(new window.Event('timelineScrollStart'));
    }
});

window.scrollTimelineToStart = function () {
    project.view.scrollBy(-scrollValue, 0);
    scrollValue = 0;
    window.dispatchEvent(new window.Event('timelineScrollStart'));
}
