$( document ).ready(function(event) {
    $('.collapser').on('click', function(event) {
        var target = $(this).children('.glyphicon-chevron');
        target.toggleClass('glyphicon-chevron-up');
        target.toggleClass('glyphicon-chevron-down');
    });
});
