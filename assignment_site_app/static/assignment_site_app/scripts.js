
$(document).ready(function () {
    $(".pawan").css("color", "blue");
    $('.pawan').hide();
    console.log('pawannnnn')

    $('.btn-filter').on('click', function () {
        console.log("here")
    });

    $('.btn-refresh').on('click', function () {
        console.log("here")
        location.reload();
    });
});
