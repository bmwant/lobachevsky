$(function() {
  console.log('we are here');
  $.get('/check_handle', function() {})
    .always(function(data, status, xhr) {
      if(xhr.status === 200) {

      }
    });
});
