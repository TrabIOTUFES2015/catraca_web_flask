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

	$('#linkCriacao').click(
		function clickLinkCriacao(argument) {
			var cmbSensorA = $('#sensorA')
			cmbSensorA.load('http://localhost:8080/sensores')
		} 
	)
	
	
});

function criarCatraca(){
	//TODO:criando catraca
	//Ir pra pagina da catraca dps de criar um objeto catraca
	//$( "#linkCatracas" ).click();
	
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


