$(function() {
  $('#is-contributor').click(function() {
    var handle = $('input[name="handle"]').val();
    var repository = $('input[name="repository"]').val();

    $.get('/check_handle', {handle: handle}, function() {})
      .always(function(data, status, xhr) {
        if(xhr.status === 200) {
          $('#handle-success').css('visibility', 'visible');
        } else {
          $('#handle-fail').css('visibility', 'visible');
        }
      });

    $.get('/check_repository', {repo: repository}, function() {})
      .always(function(data, status, xhr) {
        if(xhr.status === 200) {
          $('#repo-success').css('visibility', 'visible');
        } else {
          $('#repo-fail').css('visibility', 'visible');
        }
      });
  });
});
