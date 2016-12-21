function StudioEditSubmit(runtime, element) {

  var $element = $(element);

  $element.find('.save-button').bind('click', function() {
    var handlerUrl = runtime.handlerUrl(element, 'studio_submit');

    var usageId = $element.data('usage-id');
    var displayName = $element.find('input[name=display_name]').val();
    var displayDescription = $element.find('input[name=display_description]').val();
    var thumbnail = $element.find('input[name=thumbnail]')[0].files[0];
    var mitType = $element.find('select[name=mit_type]').val();
    var textColor = $element.find('input[name=text_color]').val();
    var headerText = $element.find('input[name=header_text]').val();
    var contentText = $element.find('textarea[name=content_text]').val().trim();
    var background = $element.find('input[name=background]')[0].files[0];

    function imagesAreValid() {
      if (thumbnail != undefined) {
        if (thumbnail.size > 2000000) {
            alert('Thumbnail size is too large!');
            false;
        }
        if (thumbnail.type.indexOf('image') !== 0) {
            alert('Thumbnail does not have a correct format!');
            false;
        }
      }
      if (background != undefined) {
        if (background.size > 8000000) {
            alert('Background image size is too large!');
            return false;
        }
        if (background.type.indexOf('image') !== 0) {
            alert('Background image does not have a correct format!');
            return false;
        }
      }
      return true;
    };
    if (!imagesAreValid()) {
      return;
    }

    var data = new FormData();
    data.append('usage_id', usageId);
    data.append('display_name', displayName);
    data.append('display_description', displayDescription);
    data.append('thumbnail', thumbnail);
    data.append('mit_type', mitType);
    data.append('text_color', textColor);
    data.append('header_text', headerText);
    data.append('content_text', contentText);
    data.append('background', background);

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
