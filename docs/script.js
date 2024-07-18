window.addEventListener("load", function(){
    var nav_elements = document.getElementsByTagName("nav")[0].getElementsByTagName("li");

    for(var i = 0; i < nav_elements.length; i++){
        var link = nav_elements[i].firstChild.getAttribute("href");

        nav_elements[i].addEventListener("click", ClicKHandler(link)); // TODO: Can this be comprehensed into a single line?

        nav_elements[i].firstChild.removeAttribute("href");
    }
});

function ClicKHandler(e) {
    return function () { callback(e) };
}

function callback(e) {
    document.getElementById(e.substr(1)).scrollIntoView({behavior: "smooth"});
}
