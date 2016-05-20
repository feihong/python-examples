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

  switch (obj.type) {
    case 'message':
      let p = $('<p></p>')
      p.text(obj.value)
      $('#messages').append(p)
      break
    case 'progress':
      $('#progress').text(`Progress: ${obj.current} out of ${obj.total}`)
      break
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
