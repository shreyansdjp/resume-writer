$(function() {
    setTimeout(function() {
        $('#message').fadeOut('slow');
    }, 3000);

    $('#changePass').click(function() {
        $('#passForm').show();
        $('#infoForm').hide();
    });

    $('#updateInfo').click(function() {
        $('#passForm').hide();
        $('#infoForm').show();
    });
});
