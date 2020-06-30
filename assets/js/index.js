AOS.init({
  duration: 1200,
})

document.body.onload = function() {
    var updating = false;
    new MutationObserver(function(mutations) {
        var title = mutations[0].addedNodes[0].nodeValue;
        if (title === "Updating...") updating = true;
        else if (title === "COVIDAnalytics" && updating == true) {
            updating = false;
            AOS.refreshHard();
            console.log("Page loaded")
        }
    }).observe(
        document.querySelector('title'),
        { subtree: true, characterData: true, childList:true }
    );
}
