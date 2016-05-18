'use strict';

$('button.ip').on('click', (evt) => {
  evt.preventDefault()
  $.get('/ip/', (data) => {
    $('#result').text('Your IP address is: ' + data)
  })
})

$('button.generate').on('click', (evt) => {
  evt.preventDefault()
  $.get('/generate/', (data) => {
    $('#result').text('Generated characters: ' + data)
  })
})
