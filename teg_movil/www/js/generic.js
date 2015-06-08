$(document).ready(function(){
    $("#profile_header").hide();

    $( ".datepicker" ).datepicker({
        changeYear: true,
        yearRange: '1900:2100'
    });

    $(document).one("pagecreate", ".multi_page", function(){
        $("#profile_header").toolbar({theme: "b", position: "fixed"});

        function navnext(next){
            $(":mobile-pagecontainer").pagecontainer("change", "#"+next, {
                transition: "slide"
            });
        }

        function navprev(prev){
            $(":mobile-pagecontainer").pagecontainer("change", "#"+prev, {
                transition: "slide",
                reverse: true
            });
        }

        $(document).on("swipeleft", ".ui-page", function(event){
            next = $(this).jqmData("next");
            if(next && (event.target === $(this)[0])){
                $('a[target='+$(this).attr("id")+']').removeClass("ui-btn-active");
                navnext(next);
            }
        });

        $(document).on("click", ".next", function(){
            next = $(this).attr("target");
            if(next)
                navnext(next);
        });

        $(document).on("swiperight", ".ui-page", function(event){
            prev = $(this).jqmData("prev");
            if(prev && (event.target === $(this)[0])){
                $('a[target='+$(this).attr("id")+']').removeClass("ui-btn-active");
                navprev(prev);
            }
        });

        $(document).on("click",".prev",function(){
            prev = $(this).attr("target");
            if(prev)
                navprev(prev);
        });
    });

    $(document).on("pageshow", ".multi_page", function(){
        thePage = $(this);
        $('a[target='+thePage.attr("id")+']').addClass("ui-btn-active");

        next = thePage.jqmData("next");
        while(next){
            $('a[target='+next+']').addClass("next");
            next = $("#"+next).jqmData("next");
        }

        prev = thePage.jqmData("prev");
        while(prev){
            $('a[target='+prev+']').addClass( "prev");
            prev = $("#"+prev).jqmData("prev");
        }

        $("#profile_header").show("fold","down");
    });

    $( "#registro_form" ).submit(function(event){
        formData = $(this).serializeArray();
        data = {};
        $(formData).each(function(index, obj){
            data[obj.name] = obj.value;
        });
        console.log(data);
    });

    $(document).on("click", "#aux", function(){
        selectTable('sgt_estado', ['id','nombre']);
        selectTable('sgt_municipio', ['id','nombre']);
        //selectTable('sgt_centroinspeccion', ['nombre']);
    });
});

// $(document).ready(function(){

//     $(document).on('swipeleft', '.ui-page', function(event){    
//         if(event.handled !== true){  // This will prevent event triggering more then once
//             var nextpage = $.mobile.activePage.next('.multi_page');
//             // swipe using id of next page if exists
//             if (nextpage.length > 0){
//                 $('[token="'+$.mobile.activePage.attr("id")+'_ref"]').removeClass("ui-btn-active");
//                 $('[token="'+nextpage.attr("id")+'_ref"]').addClass("ui-btn-active");
//                 $.mobile.changePage(nextpage, {transition: "slide", reverse: false}, true, true);
//             }
//             event.handled = true;
//         }
//         return false;         
//     });

//     $(document).on('swiperight', '.ui-page', function(event){     
//         if(event.handled !== true){ // This will prevent event triggering more then once
//             var prevpage = $(this).prev('.multi_page');
//             if (prevpage.length > 0) {
//                 $('[token="'+$.mobile.activePage.attr("id")+'_ref"]').removeClass("ui-btn-active");
//                 $('[token="'+prevpage.attr("id")+'_ref"]').addClass("ui-btn-active");
//                 $.mobile.changePage(prevpage, {transition: "slide", reverse: true}, true, true);
//             }
//             event.handled = true;
//         }
//         return false;            
//     });

//     $(document).on('click', '.change_page', function(event){
//         nextpage = $(this).attr("target");
//         $('[token="'+nextpage+'_ref"]').addClass("ui-btn-active");
//         $(this).removeClass("ui-btn-active");
//         $.mobile.changePage($('#'+nextpage), {transition: "fade"}, true, true);
//     });

// });

