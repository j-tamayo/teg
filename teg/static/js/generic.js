$(document).ready(function(){
	/* Funciones para inicializar el documento HTML */

	// Activar datepickers
	$('.date').each(function(key, value){
		init_dates($(value));
	});

});

// Activar datepickers
function init_dates(object){
	object.datepicker({
	  autoclose: true,
	  clearBtn: true,
	  language: "es",
	  startView: 1,
	});
}