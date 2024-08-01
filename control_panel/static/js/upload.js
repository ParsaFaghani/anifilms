$(function () {

  $(".js-upload-photos").click(function () {
    $("#fileupload").click();
  });

  $("#fileupload").fileupload({
    dataType: 'json',
    sequentialUploads: true,
    

    start: function (e) {
      $("#modal-progress").modal("show");
    },

    stop: function (e) {
      $("#modal-progress").modal("hide");
    },

    progressall: function (e, data) {
      var progress = parseInt(data.loaded / data.total * 100, 10);
      var strProgress = progress + "%";
      $(".progress-bar").css({"width": strProgress});
      $(".progress-bar").text(strProgress);
    },

    done: function (e, data) {
      if (data.result.is_valid) {

        $("#gallery tbody").prepend(
          "<tr><td><a href='{% url 'get_file' url %}'>{{ name }}</a></td><td><form method='post' class='commentForm' id='commentForm-{{video.id}}' name='commentForm' autocomplete='off'></form> برای تغییر صفحه را تازه سازی کنید</td></tr>"
        );
      }
    }

  });

});
