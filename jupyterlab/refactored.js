/************************** heartbeat ********************/
var base_url = document.getElementById('base_url').getAttribute('data-base_url').replace(/^\/|\/$/g, '');
var heartbeat_url = 'https://notebook.micropyramid.com/heartbeat?username=' + base_url;

var xhttp = new XMLHttpRequest();
xhttp.open("GET", heartbeat_url, true);
xhttp.send();
setInterval(function() {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", heartbeat_url, true);
    xhttp.send();
}, 30000);
/************************** heartbeat ********************/

/********************** refactored lab *********************/
//setup notebook file
//open notebook file
/********************** refactored lab *********************/
