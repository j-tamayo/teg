/* Variables Globales dedicadas al manejo del flujo y consulta de datos en la APP Móvil*/
var db;
var id_usuario = -1;
var load_data_id = 0;

/* Variables Globales Auxiliares */
var user_title = '';
var next_page = '';
var next_page_trans = '';

var meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
var dias_semana = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];

/* PROCEDIMIENTO QUE MUESTRA QUE OCURRIO UN ERROR CON UNA OPERACION EN LA BASE DE DATOS */
function errorCB(){
	console.log('Error en la transacción');
}
	
/* PROCEDIMIENTO QUE MUESTRA QUE UNA OPERACION CON LA BASE DE DATOS FUE EXITOSA */
function successCB(){
	console.log('Transacción exitosa!');
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
		tx.executeSql('create table if not exists sgt_estado(id NOT NULL, nombre character varying(255) NOT NULL, PRIMARY KEY (id));');
		tx.executeSql('create table if not exists sgt_municipio(id NOT NULL, nombre character varying(255) NOT NULL, estado integer NOT NULL, PRIMARY KEY (id), FOREIGN KEY (estado) REFERENCES sgt_estado (id))');
		tx.executeSql('create table if not exists cuentas_sgtusuario(id NOT NULL, password character varying(128) NOT NULL, apellidos character varying(200) NOT NULL, cedula character varying(100) NOT NULL, correo character varying(255) NOT NULL, direccion text NOT NULL, fecha_nacimiento date NOT NULL, nombres character varying(200) NOT NULL, sexo integer NOT NULL, telefono_local character varying(100), telefono_movil character varying(100), municipio integer, codigo_postal integer NOT NULL, PRIMARY KEY (id), FOREIGN KEY (municipio) REFERENCES sgt_municipio (id), UNIQUE (correo));');
		tx.executeSql('create table if not exists sgt_centroinspeccion(id NOT NULL, nombre character varying(255) NOT NULL, direccion text NOT NULL, municipio integer NOT NULL, capacidad integer NOT NULL, tiempo_atencion integer NOT NULL, telefonos character varying(255) NOT NULL, hora_apertura_manana time without time zone, hora_apertura_tarde time without time zone, hora_cierre_manana time without time zone, hora_cierre_tarde time without time zone, PRIMARY KEY (id), FOREIGN KEY (municipio) REFERENCES sgt_municipio (id));');
		tx.executeSql('create table if not exists sgt_tipoinspeccion(id NOT NULL, codigo character varying(50) NOT NULL, descripcion text, nombre character varying(255) NOT NULL, PRIMARY KEY (id));');
		tx.executeSql('create table if not exists sgt_estatus(id NOT NULL, nombre character varying(255) NOT NULL, codigo character varying(100) NOT NULL, PRIMARY KEY (id));');
		tx.executeSql('create table if not exists sgt_solicitudinspeccion(id NOT NULL, fecha_creacion timestamp with time zone NOT NULL, fecha_culminacion timestamp with time zone, perito character varying(200), tipo_inspeccion integer NOT NULL, usuario integer NOT NULL, estatus integer NOT NULL, centro_inspeccion integer NOT NULL, PRIMARY KEY (id), FOREIGN KEY (centro_inspeccion) REFERENCES sgt_centroinspeccion (id), FOREIGN KEY (tipo_inspeccion) REFERENCES sgt_tipoinspeccion (id), FOREIGN KEY (usuario) REFERENCES cuentas_sgtusuario (id), FOREIGN KEY (estatus) REFERENCES sgt_estatus (id));');
		tx.executeSql('create table if not exists sgt_numeroorden(id NOT NULL, asistencia integer NOT NULL, codigo character varying(50) NOT NULL, fecha_atencion date, solicitud_inspeccion integer NOT NULL, hora_atencion time without time zone, estatus integer NOT NULL, PRIMARY KEY (id), FOREIGN KEY (solicitud_inspeccion) REFERENCES sgt_solicitudinspeccion (id), FOREIGN KEY (estatus) REFERENCES sgt_estatus (id));');
		tx.executeSql('create table if not exists sgt_tipoencuesta(id NOT NULL, codigo character varying(50) NOT NULL, descripcion character varying(255) NOT NULL, PRIMARY KEY (id));');
		tx.executeSql('create table if not exists sgt_tiporespuesta(id NOT NULL, codigo character varying(50) NOT NULL, descripcion character varying(255) NOT NULL, PRIMARY KEY (id));');
		tx.executeSql('create table if not exists sgt_encuesta(id NOT NULL, descripcion text, nombre character varying(255) NOT NULL, tipo_encuesta integer, PRIMARY KEY (id), FOREIGN KEY (tipo_encuesta) REFERENCES sgt_tipoencuesta (id));');
		tx.executeSql('create table if not exists sgt_pregunta(id NOT NULL, enunciado character varying(255) NOT NULL, requerida boolean NOT NULL, tipo_respuesta integer, PRIMARY KEY (id), FOREIGN KEY (tipo_respuesta) REFERENCES sgt_tiporespuesta (id));');
		tx.executeSql('create table if not exists sgt_encuesta_preguntas(id  NOT NULL, encuesta_id integer NOT NULL, pregunta_id integer NOT NULL, PRIMARY KEY (id), FOREIGN KEY (encuesta_id) REFERENCES sgt_encuesta (id), FOREIGN KEY (pregunta_id) REFERENCES sgt_pregunta (id), UNIQUE (encuesta_id, pregunta_id))');
		tx.executeSql('create table if not exists sgt_valorposible(id NOT NULL, valor character varying(255) NOT NULL, PRIMARY KEY (id));');
		tx.executeSql('create table if not exists sgt_valorpreguntaencuesta(id NOT NULL, encuesta integer NOT NULL, pregunta integer NOT NULL, valor integer NOT NULL, orden integer NOT NULL, PRIMARY KEY (id), FOREIGN KEY (valor) REFERENCES sgt_valorposible (id), FOREIGN KEY (encuesta) REFERENCES sgt_encuesta (id), FOREIGN KEY (pregunta) REFERENCES sgt_pregunta (id));');
		tx.executeSql('create table if not exists sgt_tiponotificacion(id NOT NULL, codigo character varying(100) NOT NULL, descripcion character varying(255) NOT NULL, PRIMARY KEY (id));');
		tx.executeSql('create table if not exists sgt_notificacion(id NOT NULL, mensaje text NOT NULL, tipo_notificacion integer NOT NULL, encuesta integer, asunto character varying(255) NOT NULL, PRIMARY KEY (id), FOREIGN KEY (tipo_notificacion) REFERENCES sgt_tiponotificacion (id), FOREIGN KEY (encuesta) REFERENCES sgt_encuesta (id));');
		tx.executeSql('create table if not exists sgt_notificacionusuario(id NOT NULL, fecha_creacion timestamp with time zone NOT NULL, leida boolean NOT NULL, notificacion integer NOT NULL, usuario integer NOT NULL, PRIMARY KEY (id), FOREIGN KEY (notificacion) REFERENCES sgt_notificacion (id), FOREIGN KEY (usuario) REFERENCES cuentas_sgtusuario (id));');
	}, errorCB, loadTables);
}

function loadTables(){
	console.log("tablas cargadas exitosamente...");
	console.log("procediendo a cargar registros de la web APP...");
	
	load_data_id = 1;
	$.getJSON("http://192.168.7.126:8000/api/data-inicial/")
	.done(load_json_data)
	.fail(function(){
	    console.log("Error de conexión!");
	});
}

function dropTables(){
	db.transaction(function(tx){
		tx.executeSql('drop table sgt_notificacionusuario;');
		tx.executeSql('drop table sgt_notificacion;');
		tx.executeSql('drop table sgt_tiponotificacion;');
		tx.executeSql('drop table sgt_valorpreguntaencuesta;');
		tx.executeSql('drop table sgt_valorposible;');
		tx.executeSql('drop table sgt_encuesta_preguntas;');
		tx.executeSql('drop table sgt_pregunta;');
		tx.executeSql('drop table sgt_encuesta;');
		tx.executeSql('drop table sgt_tiporespuesta;');
		tx.executeSql('drop table sgt_tipoencuesta;');
		tx.executeSql('drop table sgt_numeroorden;');
		tx.executeSql('drop table sgt_solicitudinspeccion;');
		tx.executeSql('drop table sgt_estatus;');
		tx.executeSql('drop table sgt_tipoinspeccion;');
		tx.executeSql('drop table sgt_centroinspeccion;');
		tx.executeSql('drop table cuentas_sgtusuario;');
		tx.executeSql('drop table sgt_municipio;');
		tx.executeSql('drop table sgt_estado;');
	}, errorCB, successCB);
}

function init_data(){
	if(load_data_id == 0)
		console.log('Transacción exitosa!');

	if(load_data_id == 1){
		console.log('Inicializando páginas...');
		$('#register_page').bind('pagebeforecreate', fill_estados('SELECT id, nombre FROM sgt_estado;', 0));
		$('#create_request_page').bind('pagebeforecreate', fill_estados('SELECT DISTINCT e.id, e.nombre FROM sgt_estado e, sgt_municipio m, sgt_centroinspeccion c WHERE m.estado = e.id AND c.municipio =  m.id;', 1));
		$('#create_request_page').bind('pagebeforecreate', fill_tipos_inspeccion());
	}

	if(load_data_id == 2){
		console.log('Inicializando perfil del usuario...');
		load_profile_info();
	}
}

function load_json_data(json){
	console.log("cargando json en BD...");
	console.log(json);
	db.transaction(function(tx){
		$.each(json, function(key, value){
			$.each(value, function(table, data){
				$.each(data, function(parent_key, parent_value){
					tx.executeSql('SELECT * FROM '+table+' where id = '+parent_value.id+';', [],
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

							for(i = 0; i < results.rows.length; i++){
								row = results.rows.item(i);
								pk = row[col[0]];
								for(j = 0; j < col.length; j++){
									if(jQuery.type(val[j]) == 'boolean')
										val[j] = val[j] ? 'true' : 'false';

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
								console.log('UPDATE '+table+' SET '+str_up+' where id = '+pk+';');
								console.log(val_up);

								tx.executeSql('UPDATE '+table+' SET '+str_up+' where id = '+pk+';', val_up,
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
		});
	}, errorCB, function(){
		if(load_data_id == 1 || load_data_id == 2){ 
			console.log('Buscando datos "basura" en BD movil para realizar limpieza...');
			json = json.reverse();
			db.transaction(function(tx){
				$.each(json, function(key, value){
					$.each(value, function(table, data){
						tx.executeSql('SELECT id FROM '+table+';', [],
						function(tx, results){
							num_rows = results.rows.length;
							for(i = 0; i < num_rows; i++){
								enc = false;
								row = results.rows.item(i);
								
								$.each(data, function(parent_key, parent_value){
									if(row['id'] == parent_value['id']){
										enc = true;
										return;
									}
								});

								if(!enc){
									console.log('DELETE FROM '+table+' WHERE id = '+row['id']+';');

									tx.executeSql('DELETE FROM '+table+' WHERE id = '+row['id']+';', [],
									function(){
										console.log("registro borrado exitosamente!");
									},
									function(tx, err){
										throw new Error(err.message);
									});
								}
							}
						}, 
						function(tx, err){
							throw new Error(err.message);
						});
					});
				});
			}, errorCB, init_data);
		}
		else{
			init_data();
		}
	});
}

function load_user_tables(){
	/* Buscar y guardar información del usuario vía web service */
	console.log("login extitoso, procediendo a cargar información de usuario...");
	
	load_data_id = 2;
	$.post("http://192.168.7.126:8000/api/usuario-info/", {'id': id_usuario})
	.done(load_json_data)
	.fail(function(){
		init_data(); //cargando la data localmente...
	    console.log("Error de conexión!");
	});
}

function login(correo, password, user_info){
	aux = '';
	if(user_info['id'])
		aux = 'OR id = ' + user_info['id'];

	flag_login = false;
	db.transaction(function(tx){
	    tx.executeSql('SELECT * FROM cuentas_sgtusuario WHERE (correo = "'+correo+'" AND password = "'+password+'") '+aux+';', [], 
	    function(tx, results){
	    	num_rows = results.rows.length;
	    	if(num_rows > 0){
	    		/* Actualizar información del usuario vía web service */
	    		row = results.rows.item(0);
	    		id_usuario = row['id'];
	    		col_up = [];
	    		val_up = [];
				$.each(row, function(key, value){
					if(user_info.length){
						if(value != user_info[key]){
							col_up.push(key);
							val_up.push(user_info[key]);
						}
					}
				});

				if(val_up.length > 0)
					updateTable('cuentas_sgtusuario', col_up, val_up, 'id', id_usuario);
				
				flag_login = true;
	    	}
	    	else{
	    		if(user_info){
	    			/* Insertar información del usuario vía web service */
	    			id_usuario = user_info['id'];
	    			insertTable('cuentas_sgtusuario', 
	    						['id', 'password', 'apellidos', 'cedula', 'correo', 'direccion', 'fecha_nacimiento', 'nombres', 'sexo', 'telefono_local', 'telefono_movil', 'municipio', 'codigo_postal'],
	    						[user_info['id'], user_info['password'], user_info['apellidos'], user_info['cedula'], user_info['correo'], user_info['direccion'], user_info['fecha_nacimiento'], user_info['nombres'], user_info['sexo'], user_info['telefono_local'], user_info['telefono_movil'], user_info['municipio'], user_info['codigo_postal']]);
	    		
	    			flag_login = true;
	    		}
	    		else
	    			console.log("Usuario inválido...");
			}
	    },
		function(tx, err){
			throw new Error(err.message);
		});
	}, errorCB, function(){
		if(flag_login){
			next_page = '#profile_page';
			next_page_trans = 'flow';
			load_user_tables();
		}
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

function updateTable(table, cols, values, cond, cond_val){
	str_cols = '';
	for(i = 0; i < cols.length; i++){
		if(i > 0)
			str_cols = str_cols + ',' + cols[i] + "=?";
		else
			str_cols = str_cols + cols[i] + "=?";
	}

	console.log('UPDATE '+table+' SET '+str_cols+' WHERE '+cond+' = '+cond_val+';');
	console.log(values);
	db.transaction(function(tx){
		tx.executeSql('UPDATE '+table+' SET '+str_cols+' WHERE '+cond+' = '+cond_val+';', values,
		function(){
			console.log("registro actualizado exitosamente!");
		},
		function(tx, err){
			throw new Error(err.message);
		});
	}, errorCB, successCB);
}

function deleteTable(table, cond, cond_val){
	console.log('DELETE FROM '+table+' WHERE '+cond+' = '+cond_val+';');
	db.transaction(function(tx){
		tx.executeSql('DELETE FROM '+table+' WHERE '+cond+' = '+cond_val+';', [],
		function(){
			console.log("registro actualizado exitosamente!");
		},
		function(tx, err){
			throw new Error(err.message);
		});
	}, errorCB, successCB);
}

//Pendiente por modificar...
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

function load_profile_info(){
	$("#profile_content").empty();
	$("#request_list_content").empty();
	$("#mail_list_content").empty();

	db.transaction(function(tx){

		/* Cargando información del perfil de usuario */
		tx.executeSql('SELECT u.nombres, u.apellidos, u.cedula, u.direccion, u.correo, e.nombre AS estado, m.nombre AS municipio FROM cuentas_sgtusuario u, sgt_estado e, sgt_municipio m WHERE e.id = m.estado AND u.municipio = m.id AND u.id = '+id_usuario+';', [], 
		function(tx, results){
			row = results.rows.item(0);
			user_title = row['nombres'];

	    	$("#profile_content").html('<h3 class="text-success" style="text-align: center;">Informaci&oacute;n del usuario</h3>\
				<p>Nombre: '+row['nombres']+'</p>\
				<p>Apellido: '+row['apellidos']+'</p>\
				<p>C&eacute;dula: '+row['cedula']+'</p>\
				<p>Estado: '+row['estado']+'</p>\
				<p>Municipio: '+row['municipio']+'</p>\
				<p>Direcci&oacute;n: '+row['direccion']+'</p>\
				<p>Correo: '+row['correo']+'</p>\
				<hr>\
				<h3 class="text-success" style="text-align: center;">El usuario no posee<br>póliza asociada</h3>'	
			);	/* OJO!!! Falta cargar la información de la poliza... */
	    },
		function(tx, err){
			console.log("error");
			throw new Error(err.message);
		});
		
		/* Cargando las solicitudes realizadas por el usuario */
		tx.executeSql('SELECT s.id, n.fecha_atencion, n.hora_atencion, c.nombre AS centro_inspeccion, n.codigo, t.nombre AS tipo_inspeccion, s.perito, e.nombre AS estatus FROM sgt_solicitudinspeccion s, sgt_numeroorden n, sgt_centroinspeccion c, sgt_tipoinspeccion t, sgt_estatus e WHERE n.solicitud_inspeccion = s.id AND s.centro_inspeccion = c.id AND s.tipo_inspeccion = t.id AND s.estatus = e.id AND s.usuario = '+id_usuario+';', [], 
	    function(tx, results){
	    	num = results.rows.length;

	    	if(num > 0){
	    		aux = '<ul id="solicitudes_usuario" data-role="listview" data-inset="false" data-theme="a">';

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

					aux += '<li class="solicitud_'+row['id']+'" data-role="list-divider" data-theme="c" '+estatus_color_bg+'>'+fecha_atencion+'<span class="ui-li-count">'+hora_atencion+'</span></li>\
							<li class="solicitud_'+row['id']+'">\
								<a href="#">\
									<h2 class="text-success"><br>'+row['centro_inspeccion']+'</h2>\
									<p><strong>N&uacute;mero: '+row['codigo']+'&emsp;-&emsp;Tipo: '+row['tipo_inspeccion']+'</strong></p>\
									<p>Perito asignado: '+perito_asignado+'</p>\
									<p class="ui-li-aside '+estatus_color_text+'"><strong>'+row['estatus']+'</strong></p>\
								</a>\
								<a href="#" target-id="'+row['id']+'" class="ui-btn ui-shadow ui-icon-delete ui-nodisc-icon ui-alt-icon solicitud_item_elim"></a>\
							</li>';
				}

				aux += '</ul>';
				$('#request_list_content').html(aux).trigger('create');
			}
	    },
		function(tx, err){
			throw new Error(err.message);
		});
		
		/* Cargando las notificaciones recibidas del usuario */
		tx.executeSql('SELECT n.id AS notificacion, u.id AS notificacion_usuario, n.asunto, t.codigo, u.fecha_creacion, u.leida FROM sgt_notificacion n, sgt_tiponotificacion t, sgt_notificacionusuario u WHERE n.id = u.notificacion AND t.id = n.tipo_notificacion AND u.usuario = '+id_usuario+' ORDER BY u.leida DESC, notificacion_usuario DESC;', [], 
	    function(tx, results){
	    	num = results.rows.length;

	    	if(num > 0){
	    		aux = '<ul id="notificaciones_usuario" data-role="listview" data-split-icon="delete" data-theme="a" data-split-theme="a" data-inset="false">';

				for(i = 0; i < num; i++){
					row = results.rows.item(i);

					img_notificacion = '';
					if(row['codigo'] == 'NOTI_GEN')
						img_notificacion = 'mail-icon.png';
					if(row['codigo'] == 'NOTI_ENC')
						img_notificacion = 'poll-icon.png';
					if(row['codigo'] == 'NOTI_REC')
						img_notificacion = 'alert-icon.png';

					text = '';
					estilo = '';
					if(row['leida'] == 'true'){
						texto = 'Leida';
						estilo = 'style="background-color: #d9edf7;"';
					}
					if(row['leida'] == 'false'){
						texto = 'Nueva';
						estilo = 'style="background-color: #f0ad4e;"';
					}

					aux += '<li id="notificacion_'+row['notificacion_usuario']+'" leida="'+row['leida']+'" target-ref="'+row['notificacion']+'" fecha="'+row['fecha_creacion']+'">\
								<a href="#" target-id="'+row['notificacion_usuario']+'" class="notificacion_item"><img src="img/'+img_notificacion+'" class="ui-li-icon">\
									<h2>'+row['asunto']+'</h2>\
									<span class="ui-li-count" '+estilo+'>'+texto+'</span>\
								</a>\
								<a href="#" target-id="'+row['notificacion_usuario']+'" class="ui-nodisc-icon ui-alt-icon notificacion_item_elim"></a>\
							</li>';
				}

				aux += '</ul>';
				$('#mail_list_content').html(aux).trigger('create');
			}
	    },
		function(tx, err){
			throw new Error(err.message);
		});
		
	}, errorCB, function(){
		console.log('La información del perfil de usuario ha sido cargada exitosamente...');
		$.mobile.changePage(next_page, {
			changeHash: false, 
			transition: next_page_trans
		});
	});
}

function load_centros_inspeccion(json, sel){
	db.transaction(function(tx){
		sel.children("ul").empty();
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

function load_notificacion(id, id_ref, asunto, fecha){
	 db.transaction(function(tx){
        tx.executeSql('SELECT mensaje, encuesta FROM sgt_notificacion WHERE id = '+id+';', [], 
        function(tx, results){
        	$('#mail_title').html(asunto);
            
            row = results.rows.item(0);
            $('#mail_content').html('<p align="justify">'+row['mensaje']+'</p>');

            if(row['encuesta'])
            	$('#mail_content').append('<br><p align="left">(Recibido el '+fecha +')<p><br><button id="cargar_encuesta" target-notificacion-usuario="'+id_ref+'" target-encuesta="'+row['encuesta']+'" class="ui-btn ui-btn-c ui-corner-all" type="button">Completar encuesta</button>');

            $.mobile.changePage('#mail_content_page', {
	            changeHash: true,
	            transition: 'fade'
	        });
        },
        function(tx, err){
            throw new Error(err.message);
        });
    }, errorCB, successCB);
}

function load_encuesta(notificacion_usuario_id, encuesta_id){
	db.transaction(function(tx){
        tx.executeSql('SELECT e.nombre AS encuesta, p.id AS pregunta, p.enunciado, t.codigo AS tipo FROM sgt_encuesta e, sgt_pregunta p, sgt_tiporespuesta t, sgt_encuesta_preguntas ep WHERE e.id = ep.encuesta_id AND p.id = ep.pregunta_id AND t.id = p.tipo_respuesta AND e.id = '+encuesta_id+';', [], 
        function(tx, results){
        	aux = '';
        	index = 1;
        	row_aux = results.rows.item(0);
        	$('#mail_title').html(row_aux['encuesta']);

        	aux = '<form id="encuesta_form">\
        				<input id="usuario_enc" name="usuario" type="hidden" value="'+id_usuario+'">\
        				<input id="encuesta_enc" name="encuesta" type="hidden" value="'+encuesta_id+'">\
        				<input id="notificacion_enc" name="notificacion_usuario" type="hidden" value="'+notificacion_usuario_id+'">';

        	num = results.rows.length;
			for(i = 0; i < num; i++){
				row = results.rows.item(i);

				aux += '<div class="ui-field-contain">\
							<input id="pregunta_enc_'+(i + 1)+'" name="pregunta_'+(i + 1)+'" type="hidden" value="'+row['pregunta']+'">';

				if(row['tipo'] == 'RESP_DEF')
					aux += '<fieldset id="respuesta_def_content_'+row['pregunta']+'" data-role="controlgroup" data-iconpos="right" data-theme="a"></fieldset>';

				if(row['tipo'] == 'RESP_INDEF'){
					aux += '<label for="respuesta_indef_enc_'+index+'">'+row['enunciado']+'</label>\
							<textarea cols="40" rows="8" name="respuesta_indef_'+row['pregunta']+'" id="respuesta_indef_enc_'+index+'"></textarea>';
					index++;
				}

				aux += '</div>';
			}

			aux += '	<input id="total_preguntas_enc" name="total_preguntas" type="hidden" value="'+num+'">\
						<br><button class="ui-btn ui-btn-c ui-corner-all" type="submit">Enviar</button>\
					</form>';

			$('#mail_content').html(aux).trigger( "create" );
        },
        function(tx, err){
            throw new Error(err.message);
        });

        tx.executeSql('SELECT p.id AS pregunta, p.enunciado, v.id, v.valor FROM sgt_encuesta e, sgt_pregunta p, sgt_tiporespuesta t, sgt_valorposible v, sgt_valorpreguntaencuesta vpe, sgt_encuesta_preguntas ep WHERE e.id = ep.encuesta_id AND p.id = ep.pregunta_id AND t.id = p.tipo_respuesta AND t.codigo = "RESP_DEF" AND e.id = vpe.encuesta AND p.id = vpe.pregunta AND v.id = vpe.valor AND e.id = '+encuesta_id+' ORDER BY pregunta, vpe.orden;', [], 
        function(tx, results){
        	aux = '';
        	pregunta_index = '';

        	num = results.rows.length;
			for(i = 0; i < num; i++){
				row = results.rows.item(i);
				if(row['pregunta'] != pregunta_index){
					if(pregunta_index)
						$('#respuesta_def_content_'+pregunta_index).html(aux).trigger('create');

					pregunta_index = row['pregunta'];
					aux = '<legend>'+row['enunciado']+'</legend>';
				}

				aux += '<input name="respuesta_def_'+row['pregunta']+'" id="respuesta_def_enc_'+(i + 1)+'" value="'+row['id']+'" type="radio">\
						<label for="respuesta_def_enc_'+(i + 1)+'">'+row['valor']+'</label>';		
			}

			if(pregunta_index)
				$('#respuesta_def_content_'+pregunta_index).html(aux).trigger('create');
        },
        function(tx, err){
            throw new Error(err.message);
        });
    }, errorCB, function(){
    	console.log('Transacción exitosa!');
    	$("#encuesta_form").submit(function(event){
	        event.preventDefault();
		    formData = $(this).serializeArray();
		    data = {};

		    $(formData).each(function(index, obj){
		        data[obj.name] = obj.value;
		    });

		    $.post("http://192.168.7.126:8000/api/guardar-respuestas-encuesta/", data)
	        .done(function(json){
	            console.log(json);
	            next_page = '#mail_page';
	            next_page_trans = 'fade';
	            load_user_tables();
	        })
	        .fail(function(json) {
	            console.log(json);
	        });
	    });
    });
}

function load_user_edit_info(next_page, trans){
	db.transaction(function(tx){
        tx.executeSql('SELECT u.nombres, u.apellidos, u.sexo, u.cedula, u.correo, u.direccion, u.fecha_nacimiento, u.telefono_local, u.telefono_movil, m.estado , u.municipio, u.codigo_postal FROM cuentas_sgtusuario u, sgt_municipio m WHERE u.municipio = m.id AND u.id = '+id_usuario+';', [], 
        function(tx, results){
        	row = results.rows.item(0);

        	$('#nombres_reg').val(row['nombres']);
        	$('#apellidos_reg').val(row['apellidos']);
        	$('#cedula_reg').val(row['cedula']);
        	$('#direccion_reg').val(row['direccion']);
        	$('#codigo_postal_reg').val(row['codigo_postal']);
        	$('#telefono_local_reg').val(row['telefono_local']);
        	$('#telefono_movil_reg').val(row['telefono_movil']);
        	$('#correo_reg').val(row['correo']);

        	if(row['sexo'] == '0')
        		$('#sexo_reg0').attr('checked', 'checked').trigger('create'); //.checkboxradio('refresh');
        	if(row['sexo'] == '1')
        		$('#sexo_reg1').attr('checked', 'checked').trigger('create'); //.checkboxradio('refresh');

        	fecha_nacimiento_aux = row['fecha_nacimiento'];
        	fecha_nacimiento_aux = fecha_nacimiento_aux.split('-');
        	fecha_nacimiento_aux = fecha_nacimiento_aux[2] + '/' + fecha_nacimiento_aux[1] + '/' + fecha_nacimiento_aux[0];
        	$('#fecha_nacimiento_reg').val(fecha_nacimiento_aux);

        	estado_aux = row['estado'];
        	$('#estado_reg').val(estado_aux) //.selectmenu('refresh');

        	municipio_aux = row['municipio'];

        	tx.executeSql('SELECT m.id, m.nombre FROM sgt_estado e, sgt_municipio m WHERE e.id = m.estado AND e.id = '+estado_aux+';', [],
			function(tx, results){
				num = results.rows.length;
		    	aux = '<option value="">---Seleccione un municipio---</option>';

				for(i = 0; i < num; i++){
					row = results.rows.item(i);
					aux += '<option value="'+row['id']+'">'+row['nombre']+'</option>';
				}

				$('#municipio_reg').html(aux);
				$('#municipio_reg').val(municipio_aux);
				//$('#municipio_reg').selectmenu('refresh');

				$.mobile.changePage(next_page, {
			        changeHash: false,
			        transition: trans
			    });
			},
			function(tx, err){
				throw new Error(err.message);
			});
		},
        function(tx, err){
            throw new Error(err.message);
        });
    }, errorCB, successCB);
}