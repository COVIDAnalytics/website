AOS.init({
  duration: 1000,
  once: true,
})

document.body.onload = function() {
    var updating = false;
    new MutationObserver(function(mutations) {
        var title = mutations[0].addedNodes[0].nodeValue;
        if (title === "Updating..." && !updating) {
            updating = true;
            Array.from(document.querySelectorAll('.aos-refresh-onload')).forEach(function(element) {
                element.classList.remove("aos-animate");
            });
        }
        else if (title === "COVIDAnalytics" && updating) {
            updating = false;
            AOS.refreshHard();
            console.log("Page loaded")
        }
    }).observe(
        document.querySelector('title'),
        { subtree: true, characterData: true, childList:true }
    );
}
