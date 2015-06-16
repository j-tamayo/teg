var id_usuario;
var db;

//------------ PROCEDIMIENTO QUE MUESTRA QUE OCURRIO UN ERROR CON UNA OPERACION EN LA BASE DE DATOS
function errorCB(){
	console.log('Error en la transacción');
}
	
//------------ PROCEDIMIENTO QUE MUESTRA QUE UNA OPERACION CON LA BASE DE DATOS FUE EXITOSA
function successCB(){
	console.log('Transacción exitosa!');
}

function init_page(){
	console.log('Inicializando páginas...');
	$(".init_data").bind("pagebeforecreate", fill_estados());
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
		tx.executeSql('create table if not exists cuentas_sgtusuario(id serial NOT NULL, password character varying(128) NOT NULL, apellidos character varying(200) NOT NULL, cedula character varying(100) NOT NULL, clave character varying(255) NOT NULL, correo character varying(255) NOT NULL, direccion text NOT NULL, fecha_nacimiento date NOT NULL, nombres character varying(200) NOT NULL, sexo integer NOT NULL, telefono_local character varying(100), telefono_movil character varying(100), municipio integer, rol_id integer NOT NULL, codigo_postal integer NOT NULL, CONSTRAINT cuentas_sgtusuario_pkey PRIMARY KEY (id), CONSTRAINT cuentas_sgtus_municipio_515d51ec673e866e_fk_sgt_municipio FOREIGN KEY (municipio) REFERENCES sgt_municipio (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED, CONSTRAINT cuentas_sgtusuario_rol_id_6c992038021b9cf0_fk_cuentas_rolsgt_id FOREIGN KEY (rol_id) REFERENCES cuentas_rolsgt (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED, CONSTRAINT cuentas_sgtusuario_correo_key UNIQUE (correo));');
		tx.executeSql('create table if not exists sgt_centroinspeccion(id serial NOT NULL, nombre character varying(255) NOT NULL, direccion text NOT NULL, municipio integer NOT NULL, capacidad integer NOT NULL, tiempo_atencion integer NOT NULL, codigo character varying(20) NOT NULL, telefonos character varying(255) NOT NULL, hora_apertura_manana time without time zone, hora_apertura_tarde time without time zone, hora_cierre_manana time without time zone, hora_cierre_tarde time without time zone, CONSTRAINT sgt_centroinspeccion_pkey PRIMARY KEY (id), CONSTRAINT sgt_centroinsp_municipio_120feb748cc19ed_fk_sgt_municipio FOREIGN KEY (municipio) REFERENCES sgt_municipio (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED);');
		tx.executeSql('create table if not exists sgt_tipoinspeccion(id serial NOT NULL, codigo character varying(50) NOT NULL, descripcion text, nombre character varying(255) NOT NULL, CONSTRAINT sgt_tipoinspeccion_pkey PRIMARY KEY (id));');
		// tx.executeSql('create table if not exists sgt_solicitudinspeccion(id serial NOT NULL, fecha_creacion timestamp with time zone NOT NULL, fecha_culminacion timestamp with time zone, tipo_inspeccion_id integer NOT NULL, CONSTRAINT sgt_solicitudinspeccion_pkey PRIMARY KEY (id), CONSTRAINT sg_tipo_inspeccion_id_69234f78eec7e48a_fk_sgt_tipoinspeccion_id FOREIGN KEY (tipo_inspeccion_id) REFERENCES sgt_tipoinspeccion (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED);');
		// tx.executeSql('create table if not exists sgt_numeroorden(id serial NOT NULL, asistencia integer NOT NULL, codigo character varying(50) NOT NULL, fecha_atencion timestamp with time zone, solicitud_inspeccion_id integer NOT NULL, CONSTRAINT sgt_numeroorden_pkey PRIMARY KEY (id), CONSTRAINT "D46cf1f67ff511d5a357a31d83dde78e" FOREIGN KEY (solicitud_inspeccion_id) REFERENCES sgt_solicitudinspeccion (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED);');
		// tx.executeSql('create table if not exists sgt_encuesta(id serial NOT NULL, codigo character varying(50) NOT NULL, descripcion text, nombre character varying(255) NOT NULL, CONSTRAINT sgt_encuesta_pkey PRIMARY KEY (id));');
		// tx.executeSql('create table if not exists sgt_pregunta(id serial NOT NULL, codigo character varying(50) NOT NULL, pregunta character varying(255) NOT NULL, respuesta character varying(255) NOT NULL, CONSTRAINT sgt_pregunta_pkey PRIMARY KEY (id));');
		// tx.executeSql('create table if not exists sgt_encuesta_usuarios(id serial NOT NULL, encuesta_id integer NOT NULL, sgtusuario_id integer NOT NULL, CONSTRAINT sgt_encuesta_usuarios_pkey PRIMARY KEY (id), CONSTRAINT sgt_enc_sgtusuario_id_7f348c4d32e5a6d0_fk_cuentas_sgtusuario_id FOREIGN KEY (sgtusuario_id) REFERENCES cuentas_sgtusuario (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED, CONSTRAINT sgt_encuesta_us_encuesta_id_174f2ddb7905f1b0_fk_sgt_encuesta_id FOREIGN KEY (encuesta_id) REFERENCES sgt_encuesta (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED);');
		// tx.executeSql('create table if not exists sgt_encuesta_preguntas(id serial NOT NULL, encuesta_id integer NOT NULL, pregunta_id integer NOT NULL, CONSTRAINT sgt_encuesta_preguntas_pkey PRIMARY KEY (id), CONSTRAINT sgt_encuesta_pr_encuesta_id_41229b1c54c354f1_fk_sgt_encuesta_id FOREIGN KEY (encuesta_id) REFERENCES sgt_encuesta (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED, CONSTRAINT sgt_encuesta_pr_pregunta_id_3bf3e21f5e2fa875_fk_sgt_pregunta_id FOREIGN KEY (pregunta_id) REFERENCES sgt_pregunta (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED);');
	}, errorCB, loadTables);
}



function dropTables(){
	db.transaction(function(tx){
		// tx.executeSql("drop table sgt_encuesta_preguntas;");
		// tx.executeSql("drop table sgt_encuesta_usuarios;");
		// tx.executeSql("drop table sgt_pregunta;");
		// tx.executeSql("drop table sgt_encuesta;");
		// tx.executeSql("drop table sgt_numeroorden;");
		// tx.executeSql("drop table sgt_solicitudinspeccion;");
		tx.executeSql("drop table sgt_tipoinspeccion;");
		tx.executeSql("drop table sgt_centroinspeccion;");
		tx.executeSql("drop table cuentas_sgtusuario;");
		tx.executeSql("drop table sgt_municipio;");
		tx.executeSql("drop table sgt_estado;");
	}, errorCB, successCB);
}

function loadTables(){
	console.log("tablas cargadas exitosamente...");
	console.log("procediendo a cargar registros de la web APP...");

	$.getJSON("http://192.168.1.101:8000/api/data-inicial/")
	.done(function(json){
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
		}, errorCB, init_page);
		
	})
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
	        
	    	/* Función reservada para solicitar datos a la web APP de manera sincrona a partir de un URL */

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

	// console.log('INSERT INTO '+table+'('+str_cols+') values ('+str_values+');');
	// console.log(values);
	db.transaction(function(tx){
		tx.executeSql('INSERT INTO '+table+'('+str_cols+') values ('+str_values+');', values,
		function(){
			console.log("registro cargado exitosamente!");
		},
		function(tx, err){
			throw new Error(err.message);
		});
	}, successCB, errorCB);
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

function fill_estados(){
	db.transaction(function(tx){
		tx.executeSql('SELECT id, nombre FROM sgt_estado;', [], 
	    function(tx, results){
	    	num = results.rows.length;
	    	aux = '<option value="">---Seleccione un estado---</option>';
			for(i = 0; i < num; i++){
				row = results.rows.item(i);
				aux += '<option value="'+row['id']+'">'+row['nombre']+'</option>'
			}
			$(".estados").each(function(){
				$(this).html(aux);
				fill_municipios($(this));
			});
	    },
		function(tx, err){
			throw new Error(err.message);
		});
	}, errorCB, successCB);
}

function fill_municipios(sel_estado){
	sel_estado.bind('change', function(){
		db.transaction(function(tx){
			sel_municipio = $('#' + sel_estado.attr('target'));
			tx.executeSql('SELECT id, nombre FROM sgt_municipio WHERE estado='+sel_estado.val()+';', [], 
		    function(tx, results){
		    	num = results.rows.length;
		    	aux = '<option value="">---Seleccione un municipio---</option>';
				for(i = 0; i < num; i++){
					row = results.rows.item(i);
					aux += '<option value="'+row['id']+'">'+row['nombre']+'</option>'
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