
$(document).ready(function(){

    $(document).on('swipeleft', '.ui-page', function(event){    
        if(event.handled !== true){  // This will prevent event triggering more then once
            var nextpage = $.mobile.activePage.next('.multi_page');
            // swipe using id of next page if exists
            if (nextpage.length > 0){
                $('[token="'+$.mobile.activePage.attr("id")+'_ref"]').removeClass("ui-btn-active");
                $('[token="'+nextpage.attr("id")+'_ref"]').addClass("ui-btn-active");
                $.mobile.changePage(nextpage, {transition: "slide", reverse: false}, true, true);
            }
            event.handled = true;
        }
        return false;         
    });

    $(document).on('swiperight', '.ui-page', function(event){     
        if(event.handled !== true){ // This will prevent event triggering more then once
            var prevpage = $(this).prev('.multi_page');
            if (prevpage.length > 0) {
                $('[token="'+$.mobile.activePage.attr("id")+'_ref"]').removeClass("ui-btn-active");
                $('[token="'+prevpage.attr("id")+'_ref"]').addClass("ui-btn-active");
                $.mobile.changePage(prevpage, {transition: "slide", reverse: true}, true, true);
            }
            event.handled = true;
        }
        return false;            
    });

    $(document).on('click', '.change_page', function(event){
        nextpage = $(this).attr("target");
        $('[token="'+nextpage+'_ref"]').addClass("ui-btn-active");
        $(this).removeClass("ui-btn-active");
        $.mobile.changePage($('#'+nextpage), {transition: "fade"}, true, true);
    });

});

