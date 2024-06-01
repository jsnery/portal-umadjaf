$(document).ready(function(){
    $(".nav-link").click(function(){
        $(".nav-link").removeClass("text-dark").addClass("text-grey");
        $(this).removeClass("text-grey").addClass("text-dark");
    });
});

document.getElementById('profile-picture-image').addEventListener('click', function() {
    document.getElementById('profile_picture').click();
});


