$(document).ready(function () {
    const currentPath = window.location.pathname;

    $(".nav-link").each(function () {
        $(this).removeClass('active');
        // Check if the href matches the current path

        if ($(this).attr('href') === currentPath) {
            $(this).addClass('active fw-bold')
        }
    });
});
