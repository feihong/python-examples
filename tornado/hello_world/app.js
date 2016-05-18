'use strict';

$('button.ip').on('click', (evt) => {
  evt.preventDefault()
  $.get('/ip/', (data) => {
    alert('Your IP address is: ' + data)
  })
})
