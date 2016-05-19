'use strict';

let ws = new WebSocket('ws://' + window.location.host + '/websocket/')

ws.onopen = () => {
  console.log('Websocket opened');
}

ws.onclose = () => {
  console.log('Websocket closed');
}

ws.onmessage = (evt) => {
  let obj = JSON.parse(evt.data)

  if (obj.type === 'message') {
    let p = $('<p></p>')
    p.text(obj.value)
    $('#messages').append(p)
  }
}

$('button.start').on('click', function() {
  let value = $('input').val()
  $.get('/start/?count=' + value, (data) => {
    console.log(data)
  })
})

$('button.stop').on('click', function() {
  $.get('/stop/', (data) => {
    console.log(data)
  })
})

$('button.close').on('click', function() {
  ws.close()
})
