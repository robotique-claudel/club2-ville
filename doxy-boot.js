window.onload = function() {
    $('#main-nav').wrap('<nav class="uk-navbar-container" uk-navbar></nav>')
    $('#main-nav').wrap('<div class="uk-navbar-left"></div>')
    console.log(document.getElementById("main-menu"))
    $('#main-menu').removeClass().addClass("uk-navbar-nav")
    $('#main-menu ul').removeClass().wrap('<div class="uk-navbar-dropdown"></div>').addClass("uk-nav uk-navbar-dropdown-nav")


    $('.header').removeClass().addClass("uk-text-lead")

    $('#nav-path').remove()
   
    $(".memtitle").wrap('<article class="uk-article"></article>')
    $('.uk-article').append(function() {
        return $(this).next();
    });
    $(".memtitle").removeClass().addClass('uk-article-title')
    $(".memitem").removeClass().addClass('uk-text-lead')    
}
