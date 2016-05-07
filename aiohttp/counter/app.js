'use strict';

var ws = new WebSocket('ws://' + window.location.host + '/websocket/')

ws.onopen = () => {
  console.log('Websocket opened');
}

ws.onclose = () => {
  console.log('Websocket closed');
}

ws.onmessage = (evt) => {
  let p = $('<p></p>')
  p.text(evt.data)
  $('#messages').append(p)
}

$('#close-button').on('click', function() {
  ws.close()
})
