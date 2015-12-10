$(document).ready(function(){
	
	//transicao de pagina
	$( "nav li a" ).click(function() {
	  	  
	  var page = $(this).attr('href');
	  
	  //esconde todas as paginas
	  $('.page_info').hide();
	  //get servico ou qualquer coisa para referenciar a pagina q ta mostrando, passar page como parametro
	  //exibe a pagina clicada
	  $(page).fadeIn("slow");
	  
	  return false;	  
	  
	});	

	//transicao de pagina
	$( "#limpar" ).click(function limpaTextArea (argument) {
		var txtSaida = $('#console')
		txtSaida.val('')
		// body...
	});
	$( "#consultar" ).click(request);
    $( "#pesquisar").click(request);
	$( "#exibir").click(request);
	$( "#criar" ).click(criarCatraca);

	$('#linkCriacao').click(recarregarCmbSensores);

	$('#linkSensores').click(
		function clickLinkSensores(argument) {
			var divTabelaSensores = $('#divTabelaSensores')
			divTabelaSensores.load('http://localhost:8080/ultimasLeituras')
		}
	)

	$('#criar').click(criarCatraca);
	
	
});

function recarregarCmbSensores(argument) {
	var cmbSensorA = $('#sensorA')
	cmbSensorA.load('http://localhost:8080/sensores')

	var cmbSensorA = $('#sensorB')
	cmbSensorA.load('http://localhost:8080/sensores')
}


function criarCatraca(){

//	var sensorId1 = $('#sensorA').val()
//	var sensorId2 = $('#sensorB').val()
	var sensorId1 = $('#sensorA option:selected').attr('id');
	var sensorId2 = $('#sensorB option:selected').attr('id');


	if (sensorId1 == sensorId2) {
		alert('Impossível gerar catraca com o mesmo sensor.');
		return;
	}

	$.ajax({
		url: '/criarCatraca',
		type: 'GET',
		data: 'sensorId1=' + sensorId1 + '&sensorId2=' + sensorId2,
		success: function criarCatracaSucess(resp){
			alert('Catraca: ');
			recarregarCmbSensores();
		},
		error: function criarCatracaFail(req, status, err) {
			alert('Falhou ao criar catraca');
			console.error(err);
		}

	})

	 var page = "#page_catracas";

	  //esconde todas as paginas
	  $('.page_info').hide();

	  //exibe a pagina clicada
	  $(page).fadeIn("slow");
	  
}

function request(){

	var acao = $(this).attr("value");
		if(acao =="Limpar"){
			$("#"+acao).load('arduino.php',{acc:acao});
		}
		else{
		//$("#"+acao).load('requisicao.php',{acc:acao});
		}

}


