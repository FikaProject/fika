//Global namespace for global variables and functions. Be carefull.
fika = {};

function do_request(url, options) {
    var settings = {url: url, async: false};
    if (typeof(options) !== 'undefined') $.extend(settings, options);
    var request = $.ajax(settings);
    request.fail(function(jqXHR) {
        // So something with the fail like:
        console.log(jqXHR.status + ' ' + jqXHR.statusText);
    });
    return request;
}
fika.do_request = do_request;

$(document).ready(function(event) {
    $('.mark-course-module-done').on('click', mark_course_module_done);
    
    $('.collapser').on('click', function(event) {
        var target = $(this).children('.glyphicon-chevron');
        target.toggleClass('glyphicon-chevron-up');
        target.toggleClass('glyphicon-chevron-down');
    });

    // Slide up any messages that have the fika-auto-destruct tag
    setTimeout( function() {
        $('.fika-auto-destruct').slideUp();
    }, 3000 );
});

function mark_course_module_done(event) {
    event.preventDefault();
    var url = $(event.delegateTarget).attr('href');
    var request = fika.do_request(url);
    request.done(function(data) {
        $(event.delegateTarget).replaceWith(data);
        $('.mark-course-module-done').on('click', mark_course_module_done);
    });
}
