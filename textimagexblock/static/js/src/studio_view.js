function StudioEditSubmit(runtime, element) {
  $(element).find('.save-button').bind('click', function() {
    var handlerUrl = runtime.handlerUrl(element, 'studio_submit');
    var data = {
      display_name: $(element).find('input[name=display_name]').val(),
      mit_type: $(element).find('select[name=mit_type]').val(),
      background_url: $(element).find('input[name=background_url]').val(),
      text_color: $(element).find('input[name=text_color]').val(),
      header_text: $(element).find('input[name=header_text]').val(),
      content_text: $(element).find('textarea[name=content_text]').val().trim(),
    };
    runtime.notify('save', {state: 'start'});
    $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
      runtime.notify('save', {state: 'end'});
    });
  });

  $(element).find('.cancel-button').bind('click', function() {
    runtime.notify('cancel', {});
  });
}
