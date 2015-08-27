/* Variables Globales Auxiliares */
var page_sol = 1;

$(document).ready(function(){
    init_db();  // cargando BD Móvil...

    $('#get_password_form').hide();
    $('#profile_header').hide();
    $('#request_footer').hide();
    $('#mail_footer').hide();

    /* Inicializando elementos en las interfaces de la APP Móvil */
    $('.datepicker').datepicker({
        changeYear: true,
        yearRange: '1900:2100'
    });

    $('ul,.request,.aux').html(function(i,h){
        return h.replace(/&nbsp;/g,'');
    });

    $('#nav-panel').panel();
    $('#option_list').listview();

    /* Definición de los eventos dentro de la APP Móvil */ 
    $(document).one('pagecreate', '.multi_page', function(){
        function navnext(next){
            $(':mobile-pagecontainer').pagecontainer('change', '#' + next, {
                transition: 'slide',
                changeHash: false
            });
        }

        function navprev(prev){
            $(':mobile-pagecontainer').pagecontainer('change', '#' + prev, {
                transition: 'slide',
                changeHash: false,
                reverse: true
            });
        }

        $(document).on('swipeleft', '.ui-page', function(event){
            next = $(this).jqmData('next');
            if(next && (event.target === $(this)[0])){
                $('a[target='+$(this).attr('id')+']').removeClass('ui-btn-active');
                navnext(next);
            }
        });

        $(document).on('click', '.next', function(){
            next = $(this).attr('target');
            $(this).removeClass('next');
            if(next)
                navnext(next);
        });

        $(document).on('swiperight', '.ui-page', function(event){
            prev = $(this).jqmData('prev');
            if(prev && (event.target === $(this)[0])){
                $('a[target='+$(this).attr('id')+']').removeClass('ui-btn-active');
                navprev(prev);
            }
        });

        $(document).on('click', '.prev',function(){
            prev = $(this).attr('target');
            $(this).removeClass('prev');
            if(prev)
                navprev(prev);
        });
    });

    $(document).on('pageshow', '.multi_page', function(){
        if($('#profile_header').is(':empty')){
            $('#profile_header').css('background-color', '#000000');
            $('#profile_header').html('<div class="ui-body-b ui-body">\
                                            <h3 id="user_title">Bienvenido<br>'+user_title+'</h3>\
                                            <a href="#nav-panel" class="ui-btn ui-btn-right ui-btn-icon-left ui-icon-gear ui-corner-all">Opciones</a>\
                                            <div id="navbar_profile" data-role="navbar">\
                                                <ul id="nav">\
                                                    <li><a target="profile_page" data-icon="user">Ver Perfil</a></li>\
                                                    <li><a target="request_page" data-icon="bullets">Solicitudes</a></li>\
                                                    <li><a target="mail_page" data-icon="mail">Notificaciones</a></li>\
                                                </ul>\
                                            </div>\
                                        </div>');

            $('#profile_header').toolbar({theme: 'a', position: 'fixed'});
            $('#profile_header').show('fold', 'down').trigger('updatelayout'); 
        }

        thePage = $(this);
        link = $('a[target='+thePage.attr('id')+']');
        
        link.addClass('ui-btn-active');
        if(link.hasClass('next'))
            link.removeClass('next');
        if(link.hasClass('prev'))
            link.removeClass('prev');

        next = thePage.jqmData('next');
        while(next){
            if($('a[target='+next+']').hasClass('prev'))
                $('a[target='+next+']').removeClass('prev');

            $('a[target='+next+']').addClass('next');
            next = $('#' + next).jqmData('next');
        }

        prev = thePage.jqmData('prev');
        while(prev){
            if($('a[target='+prev+']').hasClass('next'))
                $('a[target='+prev+']').removeClass('next');

            $('a[target='+prev+']').addClass('prev');
            prev = $('#' + prev).jqmData('prev');
        }

        if(thePage.attr('id') == 'request_page')
            $('#request_footer').show('fold', 'up');

        if(thePage.attr('id') == 'mail_page')
            $('#mail_footer').show('fold', 'up');
    });

    $(document).on('pagebeforeshow', '.single_page', function(){
        if(!$('#profile_header').is(':empty')){
            $('#profile_header').hide('fold', 'up').trigger('updatelayout');
            $('#profile_header').toolbar('destroy');
            $('#profile_header').empty();
        }

        if($('#nav-panel').hasClass('ui-panel-open'))
            $('#nav-panel').panel('close');
    });

    $(document).on('pagecontainerbeforechange', function(e, data){  
        to = data.toPage;
        if(typeof to  === 'string'){
            url = $.mobile.path.parseUrl(to);
            to = url.hash || '#' + url.pathname.substring(1);
            prev_page = '#' + data.prevPage[0].id;
            from_page = '#' + data.options.fromPage[0].id;

            if($(prev_page).hasClass('multi_page') && to == '#register_page'){
                $('#usuario_reg').val(id_usuario);
                $('#register_back_btn').attr('href', '#profile_page');
            }

            if(from_page == '#login_page' && to == '#register_page'){
                $('#usuario_reg').val('');
                $('#registro_form').trigger('reset');
                $('#register_back_btn').attr('href', '#login_page');
            }

            if(from_page == '#request_page' && (to == '#mail_page' ||  to == '#profile_page' || $(to).hasClass('single_page'))){
                $('#request_footer').hide('fold', 'down');
            }

            if(from_page == '#mail_page' && (to == '#request_page' ||  to == '#profile_page' || $(to).hasClass('single_page'))){
                $('#mail_footer').hide('fold', 'down');
            }

            if(from_page == '#request_page' && to == '#create_request_page'){
                page_sol = 1;
                $('#request_form_page1').show();
                $('#request_form_page2').hide();
                $('#request_form_page3').hide();
                $('#prev_request_page').hide();
            }
        }
    });

    $(document).on('click', '.ref_btn', function(event){
        event.preventDefault();
        $.mobile.changePage($(this).attr('href'), {
            changeHash: false,
            transition: $(this).attr('data-transition')
        });
    });

    $('#registro_form').submit(function(event){
        event.preventDefault();
        formData = $(this).serializeArray();

        col_up = [];
        val_up = [];
        flag = false;
        url = '/api/usuarios/';
        if($('#usuario_reg').val()){
            flag = true;
            url = '/api/usuarios-edit/';
        }

        data = {};
        $(formData).each(function(index, obj){
            data[obj.name] = obj.value;
            if(flag){
                if(obj.name != 'usuario' && obj.name != 'estado' && obj.name != 'fecha_nacimiento' && obj.name != 'password_confirm'){
                    col_up.push(obj.name);
                    val_up.push(obj.value);
                }
            }
        });

        date_parts = data['fecha_nacimiento'].split('/');
        data['fecha_nacimiento'] = date_parts[2] + '-' + date_parts[1] + '-' + date_parts[0];
        if(flag){
            col_up.push('fecha_nacimiento');
            val_up.push(data['fecha_nacimiento']);
        }

        $(this).trigger('reset');

        $.post('http://192.168.7.126:8000'+url, data)
        .done(function(json){
            console.log('Usuario guardados exitosamente!');
            ref = $('#register_back_btn').attr('href');
            if(flag){
                updateTable('cuentas_sgtusuario', col_up, val_up, 'id', id_usuario);

                next_page = ref;
                next_page_trans = 'flip';
                load_profile_info();
            }
            else{
                $.mobile.changePage(ref, {
                    changeHash: false, 
                    transition: 'flip'
                });
            }
        })
        .fail(function(json) {
            console.log('Error de carga!');
            console.log(json.responseText);
        });
    });

    $('#login_form').submit(function(event){
        event.preventDefault();
        formData = $(this).serializeArray();

        data = {};
        $(formData).each(function(index, obj){
            data[obj.name] = obj.value;
        });

        $(this).trigger('reset');

        $.post('http://192.168.1.101:8000/api/login/', data)
        .done(function(json){
            console.log('iniciando sesión...');
            json['password'] = data['password'];
            login(data['correo'], data['password'], json);
        })
        .fail(function(json){
            if(json.status == 0){
                console.log('Error de conexión!');
                console.log('Intentando iniciar sesión localmente...');
                login(data['correo'], data['password'], {});
            }else{ //(json.status == 400)
                console.log('Usuario inválido...');
            }
        });
    });

    $('#get_password_form').submit(function(event){
        event.preventDefault();
        formData = $(this).serializeArray();

        data = {};
        $(formData).each(function(index, obj){
            data[obj.name] = obj.value;
        });

        $(this).trigger('reset');

        $.post('http://192.168.1.101:8000/api/recuperar-clave/', data)
        .done(function(json){
            updateTable('cuentas_sgtusuario', ['password'], [json['clave_temporal']], 'correo', '"'+data['correo']+'"');

            $('#get_password_form').hide('puff');
            $('#login_form').show('puff');
            $('#recordar_contraseña').show('puff');

            $('#dialog_header').html('<h1>Aviso</h1>');
            $('#dialog_content').html('<p align="justify">'+json['mensaje']+'</p>\
                                        <br>\
                                        <a href="#login_page" data-transition="pop" class="ui-btn ui-btn-b ui-corner-all ref_btn">Aceptar</a>');
            
            $.mobile.changePage('#dialog_page', {
                changeHash: false, 
                transition: 'pop'
            });
        })
        .fail(function(json) {
            console.log('Error de carga!');
            console.log(json.responseText);
        });
    });

    $('#reclamo_form').submit(function(event){
        event.preventDefault();
        formData = $(this).serializeArray();

        data = {};
        $(formData).each(function(index, obj){
            data[obj.name] = obj.value;
        });
        data['usuario'] = id_usuario;

        $(this).trigger('reset');

        $.post('http://192.168.1.101:8000/api/guardar-reclamo/', data)
        .done(function(json){
            console.log(json);
            $.mobile.changePage('#request_page', {
                changeHash: false,
                transition: 'fade'
            });
        })
        .fail(function(json){
            console.log('Error de conexión!');
        });
    });

    $(document).on('click', '#next_request_page', function(){
        if(page_sol == 3 && $('#horario_sol').val().trim()){
            data = {};
            formData = $('#request_form').serializeArray();

            $(formData).each(function(index, obj){
                data[obj.name] = obj.value;
            });

            data['usuario'] = id_usuario;
            $('#request_form').trigger('reset');
            
            $.post('http://192.168.1.101:8000/api/crear-solicitud/', data)
            .done(function(json){
                console.log(json);
                next_page = '#request_page';
                next_page_trans = 'fade';
                load_user_tables();
            })
            .fail(function(json){
                console.log('Error de conexión!');
            });
        }

        if(page_sol >= 1 && page_sol < 3){
            if(page_sol == 1 && ($('#tipo_sol').val().trim() && $('#estado_sol').val().trim() && $('#municipio_sol').val().trim() && $('#fecha_asistencia_sol').val().trim())){
                $('#request_form_page' + page_sol).hide('fade');

                page_sol++;
                $.post('http://192.168.1.101:8000/api/centros-sol/', {'municipio_id': $('#municipio_sol').val(), 'estado_id':$('#estado_sol').val()})
                .done(function(json){
                    load_centros_inspeccion(json, $('#request_form_page' + page_sol));
                })
                .fail(function(json){
                    console.log(json);
                });
            }
            else{
                if(page_sol == 2 && $('#centros_inspeccion_sol').find('a').hasClass('ui-btn-active')){
                    $('#request_form_page' + page_sol).hide('fade');
                    page_sol++;
                    $.post('http://192.168.1.101:8000/api/horarios/', {'id_centro': $('#centro_id_sol').val(), 'fecha': $('#fecha_asistencia_sol').val(), 'id_tipo_inspeccion': $('#tipo_sol').val()})
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
                        $('#horario_sol').selectmenu('refresh');
                        $('#request_form_page' + page_sol).show('fade');
                    })
                    .fail(function(json){
                        console.log(json);
                    });
                }
            }  
        }
    });

    $(document).on('click', '#prev_request_page', function(){
        if(page_sol > 1 && page_sol <= 3){
            $('#request_form_page' + page_sol).hide('fade');

            page_sol--;

            if(page_sol != 3)
                $('#next_request_page').text('Siguiente');

            if(page_sol == 1)
                $('#prev_request_page').hide('fade');

            $('#request_form_page' + page_sol).show('fade');
        }
    });

    $(document).on('click', '.centro_inspeccion_item', function(){
        $('#centro_id_sol').val($(this).attr('id'));
        $(this).closest('ul').find('a').removeClass('ui-btn-active');
        $(this).closest('ul').find('a').children('.ui-li-aside').css('color', '');
        $(this).addClass('ui-btn-active');
        $(this).children('.ui-li-aside').css('color', '#FFFFFF');
    });

    $(document).on('click', '.notificacion_item', function(){
        notificacion_usuario_id = $(this).attr('target-id');
        notificacion_item_str = '#notificacion_' + notificacion_usuario_id;
        notificacion_item_child = $(this).children('span');
        asunto = $(this).text();
        flag_leida = $(notificacion_item_str).attr('leida');
        notificacion_id = $(notificacion_item_str).attr('target-ref');
        fecha = $(notificacion_item_str).attr('fecha').replace(/-/g,'/');
        if(flag_leida == 'false'){
            $.post('http://192.168.1.101:8000/api/marcar-notificacion/', {'notificacion_usuario_id': notificacion_usuario_id, 'flag_marca': 1})
            .done(function(json){
                console.log(json);
                $(notificacion_item_str).attr('leida', 'true');
                notificacion_item_child.text('Leida');
                notificacion_item_child.attr('style', 'background-color: #d9edf7;');
                updateTable('sgt_notificacionusuario', ['leida'], ['true'], 'id', notificacion_usuario_id);
            })
            .fail(function(){
                console.log('Error de conexión!');
            });
        }
        load_notificacion(notificacion_id, notificacion_usuario_id, asunto, fecha);
    });

    $(document).on('click', '.notificacion_item_elim', function(){
        notificacion_usuario_id = $(this).attr('target-id');

        $('#dialog_header').html('<h1>Aviso</h1>');
        $('#dialog_content').html('<p align="justify">¿Est&aacute; seguro que desea eliminar esta notificaci&oacute;n?</p>\
                                    <br>\
                                    <a id="noti_elim_confirm" href="#mail_page" data-transition="pop" class="ui-btn ui-btn-b ui-corner-all">Aceptar</a>\
                                    <a href="#mail_page" data-transition="pop" class="ui-btn ui-btn-b ui-corner-all ref_btn">Cancelar</a>');
        
        $(document).on('click', '#noti_elim_confirm', function(event){
            event.preventDefault();
            ref = $(this).attr('href');
            trans = $(this).attr('data-transition');
            $.post('http://192.168.1.101:8000/api/marcar-notificacion/', {'notificacion_usuario_id': notificacion_usuario_id, 'flag_marca': 2})
            .done(function(json){
                console.log(json);
                next_page = ref;
                next_page_trans = trans;
                deleteTable('sgt_notificacionusuario', 'id', notificacion_usuario_id);
                $('#notificacion_'+notificacion_usuario_id).remove();
                $('#notificaciones_usuario').listview('refresh');
                load_user_tables();
            })
            .fail(function(){
                console.log('Error de conexión!');
            });
        });
        
        $.mobile.changePage('#dialog_page', {
            changeHash: false, 
            transition: 'pop'
        });
    });

    $(document).on('click', '.solicitud_item_elim', function(){
        solicitud_id = $(this).attr('target-id');

        $('#dialog_header').html('<h1>Aviso</h1>');
        $('#dialog_content').html('<p align="justify">¿Est&aacute; seguro que desea eliminar esta solicitud?</p>\
                                    <br>\
                                    <a id="sol_elim_confirm" href="#request_page" data-transition="pop" class="ui-btn ui-btn-b ui-corner-all">Aceptar</a>\
                                    <a href="#request_page" data-transition="pop" class="ui-btn ui-btn-b ui-corner-all ref_btn">Cancelar</a>');
        
        $(document).on('click', '#sol_elim_confirm', function(event){
            event.preventDefault();
            ref = $(this).attr('href');
            trans = $(this).attr('data-transition');
            $.post('http://192.168.1.101:8000/api/marcar-solicitud/', {'solicitud_id': solicitud_id})
            .done(function(json){
                console.log(json);
                next_page = ref;
                next_page_trans = trans;
                deleteTable('sgt_solicitudinspeccion', 'id', solicitud_id);
                $('.solicitud_'+solicitud_id).remove();
                $('#solicitudes_usuario').listview('refresh');
                load_user_tables();
            })
            .fail(function(){
                console.log('Error de conexión!');
            });
        });
        
        $.mobile.changePage('#dialog_page', {
            changeHash: false, 
            transition: 'pop'
        });
    });

    $(document).on('click', '#cargar_encuesta', function(){
        encuesta_id = $(this).attr('target-encuesta');
        notificacion_usuario_id = $(this).attr('target-notificacion-usuario');
        load_encuesta(notificacion_usuario_id, encuesta_id);
    });

    $(document).on('click', '#recordar_contraseña', function(){
        $(this).hide('puff');
        $('#login_form').hide('puff');
        $('#get_password_form').show('puff');
    });

    $(document).on('click', '#volver_login', function(){
        $('#get_password_form').hide('puff');
        $('#login_form').show('puff');
        $('#recordar_contraseña').show('puff');
    });

    $(document).on('click', '#edit_profile_option', function(event){
        event.preventDefault();
        next_page = $(this).attr('href');
        trans = $(this).attr('data-transition');
        load_user_edit_info(next_page, trans);
    });

    $(document).on('click', '#refresh_profile_option', function(){
        activePage = $.mobile.activePage.attr('id');
        next_page = '#' + activePage;
        next_page_trans = 'flow';
        load_user_tables();
    });

    $(document).on('click', '#logout_option', function(){
        id_usuario = -1;
        load_data_id = 0;

        user_title = '';
        next_page = '';
        next_page_trans = '';

        $.mobile.changePage('#login_page', {
            changeHash: false,
            transition: 'slidefade'
        });
    });
});