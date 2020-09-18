AOS.init({
  duration: 1000,
  once: true,
})

document.body.onload = function() {
    var updating = false;
    var lastURL = window.location.href;
    new MutationObserver(function(mutations) {
        var title = mutations[0].addedNodes[0].nodeValue;
        if (title === "Updating..." && !updating) {
            updating = true;

            Array.from(document.querySelectorAll('.aos-refresh-onload')).forEach(function(element) {
                element.classList.remove("aos-animate");
            });

            if (window.location.href != lastURL) {
                Array.from(document.querySelectorAll('.aos-refresh-onload-strict')).forEach(function(element) {
                    element.classList.remove("aos-animate");
                });
                lastURL = window.location.href;
            }
        }
        else if (title === "COVIDAnalytics" && updating) {
            updating = false;
            AOS.refreshHard();
            console.log("Page loaded")
            onPageLoad()
        }
    }).observe(
        document.querySelector('title'),
        { subtree: true, characterData: true, childList:true }
    );

    function onPageLoad() {
        var dropdown = document.getElementById("continent_dropdown");
        dropdown.onclick = function () {
            document.getElementById("location_map_dropdown")
                .scrollIntoView({block: "start", behavior: "smooth"});

            function openDropdown() {
                //scrolling has stopped
                var input = document.querySelector("#location_map_dropdown input")
                function injectVal(val) {
                    var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
                    nativeInputValueSetter.call(input, val);

                    var ev2 = new Event('input', { bubbles: true});
                    input.dispatchEvent(ev2);
                }
                injectVal(' ')
                injectVal('')
                window.removeEventListener("scroll", onStopScroll);
            }

            var isScrolling = "none";
            function onStopScroll(event) {
                window.clearTimeout( isScrolling );
                isScrolling = setTimeout(openDropdown, 66);
            }
            window.addEventListener('scroll', onStopScroll, false)
            setTimeout(function() {
                if (isScrolling == "none") openDropdown();
            }, 140);
        }
    }
}
