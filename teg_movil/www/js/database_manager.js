var id_usuario;
var db;
var flag_reg;

//------------ PROCEDIMIENTO QUE MUESTRA QUE OCURRIO UN ERROR CON UNA OPERACION EN LA BASE DE DATOS
function errorCB(){
	console.log('Error en la transacción!');
}
	
//------------ PROCEDIMIENTO QUE MUESTRA QUE UNA OPERACION CON LA BASE DE DATOS FUE EXITOSA
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
			dropTables();
			createTables();
			loadTables();
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
	db.transaction(function(transaction){
		transaction.executeSql('create table if not exists sgt_estado(id serial NOT NULL, nombre character varying(255) NOT NULL, CONSTRAINT sgt_estado_pkey PRIMARY KEY (id));');
		transaction.executeSql('create table if not exists sgt_municipio(id serial NOT NULL, nombre character varying(255) NOT NULL, estado_id integer NOT NULL, CONSTRAINT sgt_municipio_pkey PRIMARY KEY (id), CONSTRAINT sgt_municipio_estado_id_5aca69033bb0577_fk_sgt_estado_id FOREIGN KEY (estado_id) REFERENCES sgt_estado (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED)');
		transaction.executeSql('create table if not exists cuentas_sgtusuario(id serial NOT NULL, password character varying(128) NOT NULL, apellidos character varying(200) NOT NULL, cedula character varying(100) NOT NULL, clave character varying(255) NOT NULL, correo character varying(255) NOT NULL, direccion text NOT NULL, fecha_nacimiento date NOT NULL, nombres character varying(200) NOT NULL, sexo integer NOT NULL, telefono_local character varying(100), telefono_movil character varying(100), municipio_id integer, rol_id integer NOT NULL, codigo_postal integer NOT NULL, CONSTRAINT cuentas_sgtusuario_pkey PRIMARY KEY (id), CONSTRAINT cuentas_sgtus_municipio_id_515d51ec673e866e_fk_sgt_municipio_id FOREIGN KEY (municipio_id) REFERENCES sgt_municipio (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED, CONSTRAINT cuentas_sgtusuario_rol_id_6c992038021b9cf0_fk_cuentas_rolsgt_id FOREIGN KEY (rol_id) REFERENCES cuentas_rolsgt (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED, CONSTRAINT cuentas_sgtusuario_correo_key UNIQUE (correo));');
		transaction.executeSql('create table if not exists sgt_centroinspeccion(id serial NOT NULL, nombre character varying(255) NOT NULL, direccion text NOT NULL, municipio_id integer NOT NULL, capacidad integer NOT NULL, tiempo_atencion integer NOT NULL, codigo character varying(20) NOT NULL, telefonos character varying(255) NOT NULL, hora_apertura time without time zone, hora_cierre time without time zone, CONSTRAINT sgt_centroinspeccion_pkey PRIMARY KEY (id), CONSTRAINT sgt_centroinsp_municipio_id_120feb748cc19ed_fk_sgt_municipio_id FOREIGN KEY (municipio_id) REFERENCES sgt_municipio (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED);');
		transaction.executeSql('create table if not exists sgt_tipoinspeccion(id serial NOT NULL, codigo character varying(50) NOT NULL, descripcion text, nombre character varying(255) NOT NULL, CONSTRAINT sgt_tipoinspeccion_pkey PRIMARY KEY (id));');
		transaction.executeSql('create table if not exists sgt_solicitudinspeccion(id serial NOT NULL, fecha_creacion timestamp with time zone NOT NULL, fecha_culminacion timestamp with time zone, tipo_inspeccion_id integer NOT NULL, CONSTRAINT sgt_solicitudinspeccion_pkey PRIMARY KEY (id), CONSTRAINT sg_tipo_inspeccion_id_69234f78eec7e48a_fk_sgt_tipoinspeccion_id FOREIGN KEY (tipo_inspeccion_id) REFERENCES sgt_tipoinspeccion (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED);');
		transaction.executeSql('create table if not exists sgt_numeroorden(id serial NOT NULL, asistencia integer NOT NULL, codigo character varying(50) NOT NULL, fecha_atencion timestamp with time zone, solicitud_inspeccion_id integer NOT NULL, CONSTRAINT sgt_numeroorden_pkey PRIMARY KEY (id), CONSTRAINT "D46cf1f67ff511d5a357a31d83dde78e" FOREIGN KEY (solicitud_inspeccion_id) REFERENCES sgt_solicitudinspeccion (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED);');
		transaction.executeSql('create table if not exists sgt_encuesta(id serial NOT NULL, codigo character varying(50) NOT NULL, descripcion text, nombre character varying(255) NOT NULL, CONSTRAINT sgt_encuesta_pkey PRIMARY KEY (id));');
		transaction.executeSql('create table if not exists sgt_pregunta(id serial NOT NULL, codigo character varying(50) NOT NULL, pregunta character varying(255) NOT NULL, respuesta character varying(255) NOT NULL, CONSTRAINT sgt_pregunta_pkey PRIMARY KEY (id));');
		transaction.executeSql('create table if not exists sgt_encuesta_usuarios(id serial NOT NULL, encuesta_id integer NOT NULL, sgtusuario_id integer NOT NULL, CONSTRAINT sgt_encuesta_usuarios_pkey PRIMARY KEY (id), CONSTRAINT sgt_enc_sgtusuario_id_7f348c4d32e5a6d0_fk_cuentas_sgtusuario_id FOREIGN KEY (sgtusuario_id) REFERENCES cuentas_sgtusuario (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED, CONSTRAINT sgt_encuesta_us_encuesta_id_174f2ddb7905f1b0_fk_sgt_encuesta_id FOREIGN KEY (encuesta_id) REFERENCES sgt_encuesta (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED);');
		transaction.executeSql('create table if not exists sgt_encuesta_preguntas(id serial NOT NULL, encuesta_id integer NOT NULL, pregunta_id integer NOT NULL, CONSTRAINT sgt_encuesta_preguntas_pkey PRIMARY KEY (id), CONSTRAINT sgt_encuesta_pr_encuesta_id_41229b1c54c354f1_fk_sgt_encuesta_id FOREIGN KEY (encuesta_id) REFERENCES sgt_encuesta (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED, CONSTRAINT sgt_encuesta_pr_pregunta_id_3bf3e21f5e2fa875_fk_sgt_pregunta_id FOREIGN KEY (pregunta_id) REFERENCES sgt_pregunta (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED);');
	}, errorCB, successCB);
}

function dropTables(){
	db.transaction(function(transaction){
		transaction.executeSql("drop table sgt_encuesta_preguntas;");
		transaction.executeSql("drop table sgt_encuesta_usuarios;");
		transaction.executeSql("drop table sgt_pregunta;");
		transaction.executeSql("drop table sgt_encuesta;");
		transaction.executeSql("drop table sgt_numeroorden;");
		transaction.executeSql("drop table sgt_solicitudinspeccion;");
		transaction.executeSql("drop table sgt_tipoinspeccion;");
		transaction.executeSql("drop table sgt_centroinspeccion;");
		transaction.executeSql("drop table cuentas_sgtusuario;");
		transaction.executeSql("drop table sgt_municipio;");
		transaction.executeSql("drop table sgt_estado;");
	}, errorCB, successCB);
}

function loadTables(){
	$.getJSON("http://127.0.0.1:8000/api/estados/")
	.done(function(data){
		$.each(data, function(key, value){
			db.transaction(function(transaction){
				transaction.executeSql('INSERT INTO sgt_estado(id, nombre) values (?,?) where not exist (select * from sgt_estado where id = "'+value.id+'");', 
					[value.id, value.nombre]);
			}, successCB, errorCB);
		});
	})
	.fail(function(){
	    console.log("Error de conexión!");
	});

	$.getJSON("http://127.0.0.1:8000/api/municipios/")
	.done(function(data){
		$.each(data, function(key, value){
			db.transaction(function(transaction){
				transaction.executeSql('INSERT INTO sgt_municipio(id, nombre, estado_id) values (?,?,?) where not exist (select * from sgt_municipio where id = "'+value.id+'");', 
					[value.id, value.nombre, value.estado]);
			}, successCB, errorCB);
		});
	})
	.fail(function(){
	    console.log("Error de conexión!");
	});

	$.getJSON("http://127.0.0.1:8000/api/centros/")
	.done(function(data){
		$.each(data, function(key, value){
			db.transaction(function(transaction){
				transaction.executeSql('INSERT INTO sgt_centroinspeccion(id, nombre, direccion, capacidad, telefonos, tiempo_atencion, municipio, numero_orden, hora_apertura, hora_cierre) values (?,?,?.?,?,?,?,?,?,?) where not exist (select * from sgt_centroinspeccion where id = "'+value.id+'");', 
					[value.id, value.nombre, value.direccion, value.capacidad, value.telefonos, value.tiempo_atencion, value.municipio, value.numero_orden, value.hora_apertura, value.hora_cierre]);
			}, successCB, errorCB);
		});
	})
	.fail(function(){
	    console.log("Error de conexión!");
	});
}

function count(transaction, results){
	num = results.rows.length;
	if(num > 0)
		flag_reg = true;
	else
		flag_reg = false;
	
}

function insertTable(){

}