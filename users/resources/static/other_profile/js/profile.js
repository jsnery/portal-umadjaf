$(document).ready(function(){
    $(".nav-link").click(function(){
        $(".nav-link").removeClass("text-dark").addClass("text-grey");
        $(this).removeClass("text-grey").addClass("text-dark");
    });
});

$(document).ready(function() {
    $('.nav-item.nav-link').on('click', function() {
        // Define todos os links como não selecionados
        $('.nav-item.nav-link').attr('aria-selected', 'false');
        // Define o link clicado como selecionado
        $(this).attr('aria-selected', 'true');
    });
});

$(document).ready(function() {
    // Manipulador de clique para as abas
    $('.nav-item.nav-link').on('click', function(e) {
        e.preventDefault(); // Previne o comportamento padrão do link

        // Remove a classe 'active' e o atributo 'aria-selected' de todas as abas
        $('.nav-item.nav-link').removeClass('active').attr('aria-selected', 'false');
        // Oculta todos os conteúdos das abas
        $('.tab-content .tab-pane').removeClass('show active');

        // Adiciona a classe 'active' e o atributo 'aria-selected' na aba clicada
        $(this).addClass('active').attr('aria-selected', 'true');
        // Exibe o conteúdo correspondente à aba clicada
        var tabId = $(this).attr('href');
        $(tabId).addClass('show active');
    });
});

document.getElementById('profile-picture-image').addEventListener('click', function() {
    document.getElementById('profile_picture').click();
});


