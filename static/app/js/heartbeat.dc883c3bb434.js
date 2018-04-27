function set_heartbeat() {
    var url2 = $('#notebook').data('url2');
    $.get(url2,  function(){});
    setInterval(function() {
        var url2 = $('#notebook').data('url2');
        $.get(url2,  function(){});
    }, 10*1000);
}
set_heartbeat();
