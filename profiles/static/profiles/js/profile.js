$(document).ready(function(){
    $(".nav-link").click(function(){
        $(".nav-link").removeClass("text-dark").addClass("text-grey");
        $(this).removeClass("text-grey").addClass("text-dark");
    });
});

document.getElementById('profile-picture-image').addEventListener('click', function() {
    document.getElementById('profile_picture').click();
});



var url = 'profiles:settings';

$.get(url, function(data) {
    // Substitua 'your-element-id' pelo ID do elemento HTML no qual você deseja inserir os dados
    $('#settings-x').html(data);
});

