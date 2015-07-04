/* Variables Globales Auxiliares */
var id_usuario = -1;
var load_data_id = 0;
var db;

/* PROCEDIMIENTO QUE MUESTRA QUE OCURRIO UN ERROR CON UNA OPERACION EN LA BASE DE DATOS */
function errorCB(){
	console.log('Error en la transacción');
}
	
/* PROCEDIMIENTO QUE MUESTRA QUE UNA OPERACION CON LA BASE DE DATOS FUE EXITOSA */
function successCB(){
	console.log('Transacción exitosa!');
}

function init_data(){
	if(load_data_id == 0)
		console.log('Transacción exitosa!');

	if(load_data_id == 1){
		console.log('Inicializando páginas...');
		$(".init_data").bind("pagebeforecreate", fill_estados('SELECT id, nombre FROM sgt_estado;', 0));
		$(".init_data_sol").bind("pagebeforecreate", fill_estados('SELECT DISTINCT e.id, e.nombre FROM sgt_estado e, sgt_municipio m, sgt_centroinspeccion c WHERE m.estado = e.id AND c.municipio =  m.id;', 1));
		$(".init_data_sol").bind("pagebeforecreate", fill_tipos_inspeccion());
	}

	if(load_data_id == 2){
		console.log('Inicializando perfil del usuario...');
		$("#request_page").bind("pagebeforeshow", load_solicitudes_inspeccion());

		$.mobile.changePage("#profile_page", {
			changeHash: false, 
			transition: "flow"
		});
	}

	if(load_data_id == 3){
		console.log('Cargando nueva solicitud...');
		$("#request_page").bind("pagebeforeshow", load_solicitudes_inspeccion());

        $.mobile.changePage('#request_page', {
            changeHash: false,
            transition: 'fade'
        });
	}
}

function init_db(){
	try{
	    if(!window.openDatabase)
	        alert('Las bases de datos no son soportadas en este navegador');
	    else{
	        shortName = 'teg_movil';
	        version = '1.0';
	        displayName = 'TEG Mobile';
	        maxSize = 100 * 1024;
	        db = openDatabase(shortName, version, displayName, maxSize);

	        console.log("iniciando carga de la base de datos local...");
			//dropTables();
			createTables();
	    }
	}catch(e){
	    if(e == 2)
	        console.log("Versión inválida para la base de datos");
	    else
	        console.log("Error desconocido "+e+".");
	    return;
	}
}

function createTables(){
	db.transaction(function(tx){
		tx.executeSql('create table if not exists sgt_estado(id serial NOT NULL, nombre character varying(255) NOT NULL, CONSTRAINT sgt_estado_pkey PRIMARY KEY (id));');
		tx.executeSql('create table if not exists sgt_municipio(id serial NOT NULL, nombre character varying(255) NOT NULL, estado integer NOT NULL, CONSTRAINT sgt_municipio_pkey PRIMARY KEY (id), CONSTRAINT sgt_municipio_estado_id_5aca69033bb0577_fk_sgt_estado_id FOREIGN KEY (estado) REFERENCES sgt_estado (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED)');
		tx.executeSql('create table if not exists cuentas_sgtusuario(id serial NOT NULL, password character varying(128) NOT NULL, apellidos character varying(200) NOT NULL, cedula character varying(100) NOT NULL, correo character varying(255) NOT NULL, direccion text NOT NULL, fecha_nacimiento date NOT NULL, nombres character varying(200) NOT NULL, sexo integer NOT NULL, telefono_local character varying(100), telefono_movil character varying(100), municipio integer, codigo_postal integer NOT NULL, CONSTRAINT cuentas_sgtusuario_pkey PRIMARY KEY (id), CONSTRAINT cuentas_sgtus_municipio_515d51ec673e866e_fk_sgt_municipio FOREIGN KEY (municipio) REFERENCES sgt_municipio (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED, CONSTRAINT cuentas_sgtusuario_correo_key UNIQUE (correo));');
		tx.executeSql('create table if not exists sgt_centroinspeccion(id serial NOT NULL, nombre character varying(255) NOT NULL, direccion text NOT NULL, municipio integer NOT NULL, capacidad integer NOT NULL, tiempo_atencion integer NOT NULL, codigo character varying(20) NOT NULL, telefonos character varying(255) NOT NULL, hora_apertura_manana time without time zone, hora_apertura_tarde time without time zone, hora_cierre_manana time without time zone, hora_cierre_tarde time without time zone, CONSTRAINT sgt_centroinspeccion_pkey PRIMARY KEY (id), CONSTRAINT sgt_centroinsp_municipio_120feb748cc19ed_fk_sgt_municipio FOREIGN KEY (municipio) REFERENCES sgt_municipio (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED);');
		tx.executeSql('create table if not exists sgt_tipoinspeccion(id serial NOT NULL, codigo character varying(50) NOT NULL, descripcion text, nombre character varying(255) NOT NULL, CONSTRAINT sgt_tipoinspeccion_pkey PRIMARY KEY (id));');
		tx.executeSql('create table if not exists sgt_estatus(id serial NOT NULL, nombre character varying(255) NOT NULL, codigo character varying(100) NOT NULL, CONSTRAINT sgt_estatus_pkey PRIMARY KEY (id));');
		tx.executeSql('create table if not exists sgt_solicitudinspeccion(id serial NOT NULL, fecha_creacion timestamp with time zone NOT NULL, fecha_culminacion timestamp with time zone, perito character varying(200), tipo_inspeccion integer NOT NULL, usuario integer NOT NULL, estatus integer NOT NULL, centro_inspeccion integer NOT NULL, CONSTRAINT sgt_solicitudinspeccion_pkey PRIMARY KEY (id), CONSTRAINT "D8b278793b57d48fd3675e8c02078be7" FOREIGN KEY (centro_inspeccion) REFERENCES sgt_centroinspeccion (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED, CONSTRAINT sg_tipo_inspeccion_id_69234f78eec7e48a_fk_sgt_tipoinspeccion_id FOREIGN KEY (tipo_inspeccion) REFERENCES sgt_tipoinspeccion (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED, CONSTRAINT sgt_solici_usuario_id_7aee7c4e16426600_fk_cuentas_sgtusuario_id FOREIGN KEY (usuario) REFERENCES cuentas_sgtusuario (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED, CONSTRAINT sgt_solicitudinsp_estatus_id_3a1feabe663ac6e1_fk_sgt_estatus_id FOREIGN KEY (estatus) REFERENCES sgt_estatus (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED);');
		tx.executeSql('create table if not exists sgt_numeroorden(id serial NOT NULL, asistencia integer NOT NULL, codigo character varying(50) NOT NULL, fecha_atencion date, solicitud_inspeccion integer NOT NULL, hora_atencion time without time zone, estatus integer NOT NULL, CONSTRAINT sgt_numeroorden_pkey PRIMARY KEY (id), CONSTRAINT "D46cf1f67ff511d5a357a31d83dde78e" FOREIGN KEY (solicitud_inspeccion) REFERENCES sgt_solicitudinspeccion (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED, CONSTRAINT sgt_numeroorden_estatus_id_69d79e459cbdeeea_fk_sgt_estatus_id FOREIGN KEY (estatus) REFERENCES sgt_estatus (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED);');
		// tx.executeSql('create table if not exists sgt_encuesta(id serial NOT NULL, codigo character varying(50) NOT NULL, descripcion text, nombre character varying(255) NOT NULL, CONSTRAINT sgt_encuesta_pkey PRIMARY KEY (id));');
		// tx.executeSql('create table if not exists sgt_pregunta(id serial NOT NULL, codigo character varying(50) NOT NULL, pregunta character varying(255) NOT NULL, respuesta character varying(255) NOT NULL, CONSTRAINT sgt_pregunta_pkey PRIMARY KEY (id));');
		// tx.executeSql('create table if not exists sgt_encuesta_usuarios(id serial NOT NULL, encuesta_id integer NOT NULL, sgtusuario_id integer NOT NULL, CONSTRAINT sgt_encuesta_usuarios_pkey PRIMARY KEY (id), CONSTRAINT sgt_enc_sgtusuario_id_7f348c4d32e5a6d0_fk_cuentas_sgtusuario_id FOREIGN KEY (sgtusuario_id) REFERENCES cuentas_sgtusuario (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED, CONSTRAINT sgt_encuesta_us_encuesta_id_174f2ddb7905f1b0_fk_sgt_encuesta_id FOREIGN KEY (encuesta_id) REFERENCES sgt_encuesta (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED);');
		// tx.executeSql('create table if not exists sgt_encuesta_preguntas(id serial NOT NULL, encuesta_id integer NOT NULL, pregunta_id integer NOT NULL, CONSTRAINT sgt_encuesta_preguntas_pkey PRIMARY KEY (id), CONSTRAINT sgt_encuesta_pr_encuesta_id_41229b1c54c354f1_fk_sgt_encuesta_id FOREIGN KEY (encuesta_id) REFERENCES sgt_encuesta (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED, CONSTRAINT sgt_encuesta_pr_pregunta_id_3bf3e21f5e2fa875_fk_sgt_pregunta_id FOREIGN KEY (pregunta_id) REFERENCES sgt_pregunta (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED);');
	}, errorCB, loadTables);
}

function loadTables(){
	console.log("tablas cargadas exitosamente...");
	console.log("procediendo a cargar registros de la web APP...");
	load_data_id = 1;

	$.getJSON("http://192.168.1.101:8000/api/data-inicial/")
	.done(load_json_data)
	.fail(function(){
	    console.log("Error de conexión!");
	});
}

function dropTables(){
	db.transaction(function(tx){
		// tx.executeSql("drop table sgt_encuesta_preguntas;");
		// tx.executeSql("drop table sgt_encuesta_usuarios;");
		// tx.executeSql("drop table sgt_pregunta;");
		// tx.executeSql("drop table sgt_encuesta;");
		tx.executeSql("drop table sgt_numeroorden;");
		tx.executeSql("drop table sgt_solicitudinspeccion;");
		tx.executeSql("drop table sgt_estatus;");
		tx.executeSql("drop table sgt_tipoinspeccion;");
		tx.executeSql("drop table sgt_centroinspeccion;");
		tx.executeSql("drop table cuentas_sgtusuario;");
		tx.executeSql("drop table sgt_municipio;");
		tx.executeSql("drop table sgt_estado;");
	}, errorCB, successCB);
}

function load_json_data(json){
	console.log("cargando json en BD...");
	console.log(json);
	db.transaction(function(tx){
		$.each(json, function(table, data){
			$.each(data, function(parent_key, parent_value){
				tx.executeSql('SELECT * FROM '+table+' where id = "'+parent_value.id+'";', [],
				function(tx, results){
					val = [];
					col = [];
					first = true;
					str_cols = '';
					str_values = '';

					$.each(parent_value, function(key, value){
						val.push(value);
						col.push(key);
						if(!first){
							str_cols = str_cols + ',' + key;
							str_values = str_values + ',' + '?';
						}
						else{
							first = false;
							str_cols = str_cols + key;
							str_values = str_values + '?';
						}
					});
					flag = true;

					num_rows = results.rows.length;
					
					if(num_rows > 0){
						pk = -1;
						str_up = '';
						val_up = [];
						first = true;
						for (var i = 0; i < results.rows.length; i++){
							row = results.rows.item(i);
							pk = row[col[0]];
							for(j = 0; j < col.length; j++){
								if(row[col[j]] != val[j]){
									val_up.push(val[j]);
									if(!first)
										str_up = str_up + ', ' + col[j] + '=?';
									else{
										first = false;
										str_up = str_up + col[j] + '=?';
									}
								}
							}
						}

						if(val_up.length > 0){
							console.log('UPDATE '+table+' SET '+str_up+' where id = "'+pk+'";');
							console.log(val_up);

							tx.executeSql('UPDATE '+table+' SET '+str_up+' where id = "'+pk+'";', val_up,
							function(){
								console.log("registro actualizado exitosamente!");
							},
							function(tx, err){
								throw new Error(err.message);
							});
						}
					}
					else{
						console.log('INSERT INTO '+table+'('+str_cols+') values ('+str_values+');');
						console.log(val);

						tx.executeSql('INSERT INTO '+table+'('+str_cols+') values ('+str_values+');', val,
						function(){
							console.log("registro cargado exitosamente!");
						},
						function(tx, err){
							throw new Error(err.message);
						});
					}
				}, 
				function(tx, err){
					throw new Error(err.message);
				});
			});
		});
	}, errorCB, init_data);
}

function login(correo, password, user_info){
	db.transaction(function(tx){
	    tx.executeSql('SELECT * FROM cuentas_sgtusuario WHERE correo = "'+correo+'" AND password = '+password+';', [], 
	    function(tx, results){
	    	num_rows = results.rows.length;
	    	if(num_rows > 0){
	    		/* Actualizar información del usuario vía web service */
	    		row = results.rows.item(0);
	    		id_usuario = row['id'];
	    		col_up = [];
	    		val_up = [];
				$.each(row, function(key, value){
					if(value != user_info[key]){
						col_up.push(key);
						val_up.push(user_info[key]);
					}
				});

				if(val_up.length > 0)
					updateTable('cuentas_sgtusuario', col_up, val_up);

				load_profile_info(row);
	    	}
	    	else{
	    		if(user_info){
	    			/* Insertar información del usuario vía web service */
	    			id_usuario = user_info['id'];
	    			insertTable('cuentas_sgtusuario', 
	    						['id', 'password', 'apellidos', 'cedula', 'correo', 'direccion', 'fecha_nacimiento', 'nombres', 'sexo', 'telefono_local', 'telefono_movil', 'municipio', 'codigo_postal'],
	    						[user_info['id'], user_info['password'], user_info['apellidos'], user_info['cedula'], user_info['correo'], user_info['direccion'], user_info['fecha_nacimiento'], user_info['nombres'], user_info['sexo'], user_info['telefono_local'], user_info['telefono_movil'], user_info['municipio'], user_info['codigo_postal']]);
	    			
	    			load_profile_info(user_info);
	    		}
	    		else{
	    			console.log("Usuario inválido...");
	    			return;
	    		}
			}
	    },
		function(tx, err){
			throw new Error(err.message);
		});
	}, errorCB, load_user_tables);
}

function load_user_tables(){
	console.log("login extitoso, procediendo a cargar información de usuario...");
	load_data_id = 2;

	/* Buscar y guardar información del usuario vía web service */
	$.post("http://192.168.1.101:8000/api/usuario-info/", {'id': id_usuario})
	.done(load_json_data)
	.fail(function(){
	    console.log("Error de conexión!");
	});
}

function get_data(table, url){
	$.ajax({
	    type: "GET",
	    url: url,
	    dataType: "json",
	    async: false,
	    success: function(data){
	        
	    	/* Función AJAX reservada para solicitar datos a la web APP de manera sincrona a partir de un URL */

	    },
	    error: function(){
	    	console.log("Error de conexión!");
	    }
	});
}

function insertTable(table, cols, values){
	str_cols = '';
	str_values = '';
	for(i = 0; i < cols.length; i++){
		if(i > 0){
			str_cols = str_cols + ',' + cols[i];
			str_values = str_values + ',' + '?';
		}
		else{
			str_cols = str_cols + cols[i];
			str_values = str_values + '?';
		} 
	}

	console.log('INSERT INTO '+table+'('+str_cols+') values ('+str_values+');');
	console.log(values);
	db.transaction(function(tx){
		tx.executeSql('INSERT INTO '+table+'('+str_cols+') values ('+str_values+');', values,
		function(){
			console.log("registro cargado exitosamente!");
		},
		function(tx, err){
			throw new Error(err.message);
		});
	}, errorCB, successCB);
}

function updateTable(table, cols, values){
	str_cols = '';
	for(i = 0; i < cols.length; i++){
		if(i > 0)
			str_cols = str_cols + ',' + cols[i] + "=?";
		else
			str_cols = str_cols + cols[i] + "=?";
	}

	console.log('UPDATE '+table+' SET '+str_cols+' where id = "'+id_usuario+'";');
	console.log(values);
	db.transaction(function(tx){
		tx.executeSql('UPDATE '+table+' SET '+str_cols+' where id = "'+id_usuario+'";', values,
		function(){
			console.log("registro actualizado exitosamente!");
		},
		function(tx, err){
			throw new Error(err.message);
		});
	}, errorCB, successCB);
}

function selectTable(table, cols){
	str_cols = '';
	for(i = 0; i < cols.length; i++){
		if(i > 0)
			str_cols = str_cols + ', ' + cols[i];
		else
			str_cols = str_cols + cols[i];
	}

	db.transaction(function(tx){
	    tx.executeSql('SELECT '+str_cols+' FROM '+table+' WHERE id=1;', [], 
	    function(tx, results){
	    	num = results.rows.length;
			for(i = 0; i < num; i++){
				row = results.rows.item(i);
				console.log(row);
			}
	    },
		function(tx, err){
			throw new Error(err.message);
		});
	});
}

/* Funciones definidas para la carga inicial de datos en la APP móvil */
function fill_estados(query, flag){
	db.transaction(function(tx){
		tx.executeSql(query, [], 
	    function(tx, results){
	    	num = results.rows.length;
	    	aux = '<option value="">---Seleccione un estado---</option>';
			for(i = 0; i < num; i++){
				row = results.rows.item(i);
				aux += '<option value="'+row['id']+'">'+row['nombre']+'</option>';
			}

			sel_estados = '.estados'
			query_municipio = 'SELECT id, nombre FROM sgt_municipio WHERE estado = ';
			if(flag == 1){
				sel_estados = '.estados_centros';
				query_municipio = 'SELECT DISTINCT m.id, m.nombre FROM sgt_estado e, sgt_municipio m, sgt_centroinspeccion c WHERE m.estado = e.id AND c.municipio =  m.id AND e.id = ';
			}

			$(sel_estados).each(function(){
				$(this).html(aux);
				fill_municipios($(this), query_municipio);
			});
	    },
		function(tx, err){
			throw new Error(err.message);
		});
	}, errorCB, successCB);
}

function fill_municipios(sel_estado, query){
	sel_estado.bind('change', function(){
		db.transaction(function(tx){
			sel_municipio = $('#' + sel_estado.attr('target'));
			tx.executeSql(query+sel_estado.val()+';', [], 
		    function(tx, results){
		    	num = results.rows.length;
		    	aux = '<option value="">---Seleccione un municipio---</option>';
				for(i = 0; i < num; i++){
					row = results.rows.item(i);
					aux += '<option value="'+row['id']+'">'+row['nombre']+'</option>';
				}
				sel_municipio.html(aux);
				sel_municipio.selectmenu("refresh");
		    },
			function(tx, err){
				console.log("error");
				throw new Error(err.message);
			});
		}, errorCB, successCB);
	});
}

function fill_tipos_inspeccion(){
	db.transaction(function(tx){
		tx.executeSql('SELECT id, nombre FROM sgt_tipoinspeccion;', [], 
	    function(tx, results){
	    	num = results.rows.length;
	    	aux = '<option value="">---Seleccione un tipo---</option>';
			for(i = 0; i < num; i++){
				row = results.rows.item(i);
				aux += '<option value="'+row['id']+'">'+row['nombre']+'</option>';
			}
			$(".tipos_inspeccion").each(function(){
				$(this).html(aux);
			});
	    },
		function(tx, err){
			throw new Error(err.message);
		});
	}, errorCB, successCB);
}

function load_profile_info(user_info){
	$("#user_title").html('Bienvenido<br>'+user_info['nombres']);
	db.transaction(function(tx){
		tx.executeSql('SELECT e.nombre as estado, m.nombre as municipio FROM sgt_estado e, sgt_municipio m WHERE e.id = m.estado AND m.id = '+user_info['municipio']+';', [], 
	    function(tx, results){
	    	row = results.rows.item(0);
	    	console.log(row);
	    	$("#profile_page").children(".ui-content").html('<h3 class="text-success" style="text-align: center;">Informaci&oacute;n del usuario</h3>\
				<p>Nombre: '+user_info['nombres']+'</p>\
				<p>Apellido: '+user_info['apellidos']+'</p>\
				<p>C&eacute;dula: '+user_info['cedula']+'</p>\
				<p>Estado: '+row['estado']+'</p>\
				<p>Municipio: '+row['municipio']+'</p>\
				<p>Direcci&oacute;n: '+user_info['direccion']+'</p>\
				<p>Correo: '+user_info['correo']+'</p>\
				<hr>\
				<h3 class="text-success" style="text-align: center;">El usuario no posee<br>póliza asociada</h3>'	
			);
	    },
		function(tx, err){
			console.log("error");
			throw new Error(err.message);
		});
	}, errorCB, successCB);
}

function load_centros_inspeccion(json, sel){
	db.transaction(function(tx){
		sel.children("ul").html('');
		$(json).each(function(key, value){
			tx.executeSql('SELECT nombre, telefonos, direccion FROM sgt_centroinspeccion WHERE id = '+value['id']+';', [], 
		    function(tx, results){
		   		aux = '';
		   		num_rows = results.rows.length;
		   		for(var i = 0; i < results.rows.length; i++){
					row = results.rows.item(i);
					aux += '<li><a id='+value['id']+' disp='+value['disponibilidad']+' href="#" class="centro_inspeccion_item">\
								<br><h2>'+row['nombre']+'</h2>\
                                <p><strong>Tel&eacute;fonos: </strong>'+row['telefonos']+'</p>\
                                <p><strong>Direcci&oacute;n: </strong>'+row['direccion']+'</p>\
                                <p class="ui-li-aside text-'+value['etiqueta_clase']+'"><strong>Disponibilidad: '+value['etiqueta']+'</strong></p>\
                                </a>\
							</li>';
				}

				sel.children("ul").append(aux);
				sel.children("ul").html(function(i,h){
			        return h.replace(/&nbsp;/g,'');
			    });
				sel.children("ul").listview("refresh");

				sel.show("fade");
				$("#prev_request_page").show("fade");
		    },
			function(tx, err){
				throw new Error(err.message);
			});
		});
	}, errorCB, successCB);
}

var meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
var dias_semana = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];

function load_solicitudes_inspeccion(){
	flag_refresh = $('#request_list').is(':empty');
	db.transaction(function(tx){
		$('#request_list').html('');
		tx.executeSql('SELECT n.fecha_atencion, n.hora_atencion, c.nombre AS centro_inspeccion, n.codigo, t.nombre AS tipo_inspeccion, s.perito, e.nombre AS estatus FROM cuentas_sgtusuario u, sgt_numeroorden n, sgt_solicitudinspeccion s, sgt_centroinspeccion c, sgt_tipoinspeccion t, sgt_estatus e WHERE n.solicitud_inspeccion = s.id AND s.centro_inspeccion = c.id AND s.tipo_inspeccion = t.id AND s.estatus = e.id AND u.id ='+id_usuario+';', [], 
	    function(tx, results){
	    	aux = '';
	    	num = results.rows.length;
			for(i = 0; i < num; i++){
				row = results.rows.item(i);

				fecha_atencion = row['fecha_atencion'].split('-');
				fecha_atencion = new Date(fecha_atencion[2] + '-' + fecha_atencion[1] + '-' + fecha_atencion[0]);
				fecha_atencion = dias_semana[fecha_atencion.getDay()] + ", " + fecha_atencion.getDate() + " de " + meses[fecha_atencion.getMonth()] + " del " + fecha_atencion.getFullYear();

				hora_atencion = row['hora_atencion'].split(':');
				hora_aux = parseInt(hora_atencion[0]);
				
				am_pm = 'AM';
				if(hora_aux > 11)
					am_pm = 'PM';

				if(hora_aux >= 12)
					hora_aux = hora_aux - 12;

				hora_atencion = hora_aux + ':' + hora_atencion[1] + ' ' + am_pm;

				estatus_color_bg = '';
				estatus_color_text = 'text-primary';
				if(row['estatus'] == 'solicitud_en_proceso'){
					estatus_color_bg = 'class = "brand-warning"';
					estatus_color_text = 'text-warning';
				}
				if(row['estatus'] == 'solicitud_no_procesada'){
					estatus_color_bg = 'class = "brand-danger"';
					estatus_color_text = 'text-danger';
				}

				perito_asignado = row['perito'];
				if(perito_asignado == '')
					perito_asignado = 'N/A'; 

				aux += '<li data-role="list-divider" data-theme="c" '+estatus_color_bg+'>'+fecha_atencion+'<span class="ui-li-count">'+hora_atencion+'</span></li>\
						<li>\
							<a href="#">\
								<h2 class="text-success"><br>'+row['centro_inspeccion']+'</h2>\
								<p><strong>N&uacute;mero: '+row['codigo']+'&emsp;-&emsp;Tipo: '+row['tipo_inspeccion']+'</strong></p>\
								<p>Perito asignado: '+perito_asignado+'</p>\
								<p class="ui-li-aside '+estatus_color_text+'"><strong>'+row['estatus']+'</strong></p>\
							</a>\
							<a href="#" class="ui-btn ui-shadow ui-icon-delete ui-nodisc-icon ui-alt-icon"></a>\
						</li>';
			}
			$('#request_list').html(aux);

			if(!flag_refresh)
				$('#request_list').listview("refresh");
	    },
		function(tx, err){
			throw new Error(err.message);
		});
	}, errorCB, successCB);
}