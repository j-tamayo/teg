$(document).ready(function(){
    init_db();
    
    $('request_content').css('margin: -1 0');

    $("#profile_header").hide();
    $("#request_footer").hide();

    $(".datepicker").datepicker({
        changeYear: true,
        yearRange: '1900:2100'
    });

    $("#fecha_asistencia_sol").datepicker({
        changeYear: true,
        yearRange: '1900:2100'
    });

    $('ul,.request,.aux').html(function(i,h){
        return h.replace(/&nbsp;/g,'');
    });

    /* Variables auxiliares */
    var page_sol = 1;

    $(document).one("pagecreate", ".multi_page", function(){
        $("#profile_header").toolbar({theme: "b", position:"fixed"});

        function navnext(next){
            $(":mobile-pagecontainer").pagecontainer("change", "#" + next, {
                transition: "slide",
                changeHash: false
            });
        }

        function navprev(prev){
            $(":mobile-pagecontainer").pagecontainer("change", "#" + prev, {
                transition: "slide",
                changeHash: false,
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
            $(this).removeClass("next");
            if(next)
                navnext(next);
        });

        $(document).on("swiperight", ".ui-page", function(event){
            prev = $(this).jqmData("prev");
            //console.log(next);
            if(prev && (event.target === $(this)[0])){
                $('a[target='+$(this).attr("id")+']').removeClass("ui-btn-active");
                navprev(prev);
            }
        });

        $(document).on("click",".prev",function(){
            prev = $(this).attr("target");
            $(this).removeClass("prev");
            if(prev)
                navprev(prev);
        });
    });

    $(document).on("pageshow", ".multi_page", function(){
        thePage = $(this);
        link = $('a[target='+thePage.attr("id")+']');
        
        link.addClass("ui-btn-active");
        if(link.hasClass("next"))
            link.removeClass("next");
        if(link.hasClass("prev"))
            link.removeClass("prev");

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

        if(thePage.attr("id") == "request_page")
            $("#request_footer").show("fold","up");

        $("#profile_header").show("fold","down");
    });

    $(document).on('pagecontainerbeforechange', function(e, data){  
        to = data.toPage;
        if(typeof to  === 'string'){
            url = $.mobile.path.parseUrl(to);
            to = url.hash || '#' + url.pathname.substring(1);
            prev_page = '#' + data.prevPage[0].id;
            from_page = '#' + data.options.fromPage[0].id;

            //console.log(data.options);
            if($(prev_page).hasClass("multi_page") && data.options.direction == "back"){
                $("#profile_header").hide("fold","down");
                //window.location.replace("#login_page");

                //data.toPage = "#login_page";
                //data.prevPage = $("#login_page");
                // var lent = history.length - 1; //count total row in history
                // history.go(-lent); //destroy all history and make it as null
                
                //window.history.go((-2)); 
                //e.preventDefault();
                //e.stopPropagation();
            }

            if(from_page == "#request_page" && (to == "#mail_page" ||  to == "#profile_page")){
                $("#request_footer").hide("fold","down");
            }

            if(from_page == "#request_page" && to == "#create_request_page"){
                page_sol = 1;
                $("#request_form_page1").show();
                $("#request_form_page2").hide();
                $("#request_form_page3").hide();
                $("#prev_request_page").hide();
                $("#profile_header").toolbar("disable");
                $("#profile_header").hide("fold","up");
            }

            if(from_page == "#create_request_page" && to == "#request_page"){
                //console.log("hi!!!");
                //$("#profile_header").toolbar("enable");
                $("#profile_header").show("fold","down");
            }
        }
    });

    $("#registro_form").submit(function(event){
        event.preventDefault();
        formData = $(this).serializeArray();
        console.log(formData);
        data = {};
        $(formData).each(function(index, obj){
            data[obj.name] = obj.value;
        });

        date_parts = data['fecha_nacimiento'].split('/');
        data['fecha_nacimiento'] = date_parts[2] + '-' + date_parts[1] + '-' + date_parts[0];

        $.post("http://192.168.1.101:8000/api/usuarios/", data)
        .done(function(json){
            console.log("Usuario guardados exitosamente!");
            $.mobile.changePage("#login_page", {
                changeHash: false, 
                transition: "flip"
            });
        })
        .fail(function(json) {
            console.log("Error de carga!");
            console.log(json.responseText);
        });
    });

    $("#login_form").submit(function(event){
        event.preventDefault();
        formData = $(this).serializeArray();
        console.log(formData);
        data = {};
        $(formData).each(function(index, obj){
            data[obj.name] = obj.value;
        });

        $.post("http://192.168.1.101:8000/api/login/", data)
        .done(function(json){
            console.log("iniciando sesión...");
            json['password'] = data['password'];
            login(data['correo'], data['password'], json);
        })
        .fail(function(json){
            if(json.status == 0){
                console.log("Error de conexión!");
                console.log("Intentando iniciar sesión localmente...");
                login(data['correo'], data['password'], {});
            }else{ //(json.status == 400)
                console.log("Usuario inválido...");
            }
        });
    });

    $(document).on("click", ".back_btn", function(){
        event.preventDefault();
        $.mobile.changePage($(this).attr('href'), {
            changeHash: false,
            transition: $(this).attr('data-transition')
        });
    });

    
    $(document).on("click", "#next_request_page", function(){
        if(page_sol == 3){
            data = {};
            formData = $('#request_form').serializeArray();

            $(formData).each(function(index, obj){
                data[obj.name] = obj.value;
            });

            //date_parts = data['fecha_asistencia'].split('/');
            //data['fecha_asistencia'] = date_parts[2] + '-' + date_parts[1] + '-' + date_parts[0];
            data['usuario'] = id_usuario;

            $.post("http://192.168.1.101:8000/api/crear-solicitud/", data)
            .done(function(json){
                
                /* Refrescar lista de solicitudes */

                $('#request_form').trigger('reset');
                $('#next_request_page').text('Siguiente');
                $.mobile.changePage('#request_page', {
                    changeHash: false,
                    transition: 'fade'
                });
            })
            .fail(function(json){
                console.log("Error de conexión!");
            });
        }

        if(page_sol >= 1 && page_sol < 3){
            $("#request_form_page"+page_sol).hide("fade");
            
            page_sol++;

            if(page_sol == 1)
                $("#request_form_page"+page_sol).show("fade");

            if(page_sol == 2){
                $.post("http://192.168.1.101:8000/api/centros-sol/", {'municipio_id': $('#municipio_sol').val(), 'estado_id':$('#estado_sol').val()})
                .done(function(json){
                    load_centros_inspeccion(json, $("#request_form_page"+page_sol));
                })
                .fail(function(json){
                    console.log(json);
                });
            }

            if(page_sol == 3){
                $.post("http://192.168.1.101:8000/api/horarios/", {'id_centro': $('#centro_id_sol').val(), 'fecha': $('#fecha_asistencia_sol').val(), 'id_tipo_inspeccion': $('#tipo_sol').val()})
                .done(function(json){
                    $('#preview_centro').text($($('#centros_inspeccion_sol').children('li').find('a.ui-btn-active')).children('h2').text());
                    $('#preview_fecha_sol').text($('#fecha_asistencia_sol').val());
                    $('#preview_estado_sol').text($('#estado_sol :selected').text());
                    $('#preview_municipio_sol').text($('#municipio_sol :selected').text());

                    $('#next_request_page').text('Enviar');

                    aux = '<option value="">---Seleccione un tipo---</option>';
                    $(json).each(function(key, value){
                        aux += '<option value="'+value['value']+'">'+value['text']+'</option>';
                    });
                    $('#horario_sol').html(aux);
                    $('#horario_sol').selectmenu("refresh");
                    $("#request_form_page"+page_sol).show("fade");
                })
                .fail(function(json){
                    console.log(json);
                });
            }  
        }
        console.log(page_sol);
    });

    $(document).on("click", "#prev_request_page", function(){
        if(page_sol > 1 && page_sol <= 3){
            $("#request_form_page"+page_sol).hide("fade");

            page_sol--;

            if(page_sol != 3)
                $('#next_request_page').text('Siguiente');

            if(page_sol == 1)
                $("#prev_request_page").hide("fade");

            $("#request_form_page"+page_sol).show("fade");
        }
        console.log(page_sol);
    });

    $(document).on("click", ".centro_inspeccion_item", function(){
        $(this).closest('ul').find('a').removeClass('ui-btn-active');
        $(this).addClass('ui-btn-active');
        $('#centro_id_sol').val($(this).attr('id'));
    });

    $(document).on("click", "#aux", function(){
        //$("#profile_header").hide();
        //alert(selectTable('sgt_estado', ['id','nombre']));
        //selectTable('sgt_centroinspeccion', ['nombre']);
    });
});

/* Funcion declarada para el manejo de eventos relacionados con la navegacion */
// $(function(){
//     $(window).hashchange(function(){
//         hash = location.hash;
//         //console.log('<------------cambio de pag----------->');
//         $( "#nav li a" ).each(function(){
//             that = $(this);
//             aux = '#' + that.attr( "target" );
//             //console.log(aux + '->' + (aux === hash ? "addClass" : "removeClass"));
//             that[ aux === hash ? "addClass" : "removeClass" ]("ui-btn-active");
//         });
//     });

//     $(window).hashchange();


    //Respond to back/forward navigation
    // $(window).on("navigate", function(event, data){
    //     // if(data.state.foo) {
    //     //     // Make use of the arbitrary data stored
    //     // }

    //     // // console.log( data.state.info );
    //     // // console.log( data.state.direction );
    //     // // console.log( data.state.url );
    //     // //console.log( data.state.hash );

    //     // if(data.state.direction == "back"){
            
           
    //     //     // Make use of the directional information
    //     // }

    //     // reset the content based on the url
    //     //alterContent(data.state.url);
    // });
//});

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