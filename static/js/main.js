$(function() {
  var xhrHandle = null,
    xhrRepo = null;

  var handleSuccess = $('#handle-success'),
    handleFail = $('#handle-fail'),
    repoSuccess = $('#repo-success'),
    repoFail = $('#repo-fail');

  $('input[name="handle"]').keyup(function(e) {
    var handle = $(this).val();
    handleSuccess.css('opacity', 0);
    handleFail.css('opacity', 0);
    if(xhrHandle !== null) xhrHandle.abort();
    xhrHandle = $.get('/check_handle', {handle: handle}, function () {})
      .always(function (data, status, xhr) {
        if (xhr.status === 200) {
          handleSuccess.css('opacity', 1);
          handleFail.css('opacity', 0);
        } else {
          handleFail.css('opacity', 1);
          handleSuccess.css('opacity', 0);
        }
      });
  });

  $('input[name="repository"]').keyup(function(e) {
    var repository = $(this).val();
    repoSuccess.css('opacity', 'hidden');
    repoFail.css('opacity', 'hidden');
    if(xhrRepo !== null) xhrRepo.abort();
    xhrRepo = $.get('/check_repository', {repo: repository}, function () {})
      .always(function (data, status, xhr) {
        if (xhr.status === 200) {
          repoSuccess.css('opacity', 1);
          repoFail.css('opacity', 0);
        } else {
          repoFail.css('opacity', 1);
          repoSuccess.css('opacity', 0);
        }
      });
  });


  var resultsModal = $('#results-modal'),
    overlay = $('#overlay');

  $('#is-contributor').click(function() {
    // todo: add spinner
    var handle = $('input[name="handle"]').val();
    var repository = $('input[name="repository"]').val();

    $.getJSON('/check_contributor', {
      handle: handle,
      repo: repository
    }, function(data) {
      resultsModal.addClass('in');
      overlay.show();
      $('.modal-text').text(data.message);
      if(data.contributor) {
        $('#contributor-btn').show();
      } else {
        $('#impostor-btn').show();
      }
    });
  });

  $('.res-buttons .siimple-btn').click(function() {
    resultsModal.removeClass('in');
    overlay.hide();
  });
});
