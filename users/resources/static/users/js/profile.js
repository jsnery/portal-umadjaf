// Inicialização do documento
$(document).ready(function(){
    // Alteração de cores nos links de navegação
    $(".nav-link").click(function(){
        $(".nav-link").removeClass("text-dark").addClass("text-grey");
        $(this).removeClass("text-grey").addClass("text-dark");
    });
});

// Manipulação de atributos ARIA para acessibilidade
$(document).ready(function() {
    $('.nav-item.nav-link').on('click', function() {
        $('.nav-item.nav-link').attr('aria-selected', 'false');
        $(this).attr('aria-selected', 'true');
    });
});

// Controle de abas e conteúdo associado
$(document).ready(function() {
    $('.nav-item.nav-link').on('click', function(e) {
        e.preventDefault();

        $('.nav-item.nav-link').removeClass('active').attr('aria-selected', 'false');
        $('.tab-content .tab-pane').removeClass('show active');

        $(this).addClass('active').attr('aria-selected', 'true');
        var tabId = $(this).attr('href');
        $(tabId).addClass('show active');
    });
});

// Manipulação de clique para imagem de perfil
document.getElementById('profile-picture-image').addEventListener('click', function() {
    document.getElementById('profile_picture').click();
});

// Carregamento de configurações de perfil
$(document).ready(function() {
    var url = 'profiles:settings';

    $.get(url, function(data) {
        $('#settings-x').html(data);
    });
});

// Exibição de botão flutuante em aba específica
$(document).ready(function() {       
    $('#nav-posts-tab').click(function() {
        $('#float-btn').show();
    });

    $('.nav-item.nav-link').not('#nav-posts-tab').click(function() {
        $('#float-btn').hide();
    });
});
