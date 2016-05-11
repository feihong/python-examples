'use strict';

var ws = new WebSocket('ws://' + window.location.host + '/status/')

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

$('button.start').on('click', function(evt) {
  evt.preventDefault()
  $.get('/start-task/?' + $('form').serialize(), (data) => {
    console.log(data)
  })
})

$('button.stop').on('click', function(evt) {
  evt.preventDefault()
  $.get('/stop-task/?' + $('form').serialize(), (data) => {
    console.log(data)
  })
})
