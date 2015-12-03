$(document).ready(function(){
            if (!!window.EventSource) {
                console.log('SSE supported.');
                var source = new EventSource('http://localhost:8080/barcode');

                source.addEventListener('message', function(e) {
                  //console.log(e.data);
                  var txtSaida = $('#console')
                  var s = txtSaida.val() + '\n' + e.data
                  txtSaida.val(s)

                }, false);

                source.addEventListener('open', function(e) {
                  console.log('Connection was opened.');
                }, false);

                source.addEventListener('error', function(e) {
                  if (e.readyState == EventSource.CLOSED) {
                    console.log('Connection was closed.');
                  }
                }, false);

            } else {
                console.log('SSE notsupported.');
            }
        });
