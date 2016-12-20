function StudioEditSubmit(runtime, element) {

  var $element = $(element);

  $element.find('.save-button').bind('click', function() {
    var handlerUrl = runtime.handlerUrl(element, 'studio_submit');

    var data = new FormData();
    data.append('usage_id', $element.data('usage-id'));
    data.append('display_name', $element.find('input[name=display_name]').val());
    data.append('display_description', $element.find('input[name=display_description]').val());
    data.append('thumbnail', $element.find('input[name=thumbnail]')[0].files[0]);
    data.append('mit_type', $element.find('select[name=mit_type]').val());
    data.append('text_color', $element.find('input[name=text_color]').val());
    data.append('header_text', $element.find('input[name=header_text]').val());
    data.append('content_text', $element.find('textarea[name=content_text]').val().trim());
    data.append('background', $element.find('input[name=background]')[0].files[0]);

    //file size in bytes
    if (data.get('thumbnail').size > 2000000) {
        alert('Thumbnail size is too large!');
        return;
    }

    if (data.get('background').size > 8000000) {
        alert('Background image size is too large!');
        return;
    }

    if (data.get('thumbnail').type.indexOf('image') !== 0) {
        alert('Thumbnail does not have a correct format!');
        return;
    }

    if (data.get('background').type.indexOf('image') !== 0) {
        alert('Background image does not have a correct format!');
        return;
    }

    runtime.notify('save', {state: 'start'});

    $.ajax({
      url: handlerUrl,
      type: 'POST',
      data: data,
      cache: false,
      dataType: 'json',
      processData: false,
      contentType: false
    }).done(function(response) {
      runtime.notify('save', {state: 'end'});
    });
  });

  $element.find('.cancel-button').bind('click', function() {
    runtime.notify('cancel', {});
  });
}
