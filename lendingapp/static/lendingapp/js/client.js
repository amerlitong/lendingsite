$(function () {
  $(".js-add-client").click(function () {
    $.ajax({
      url: '/lending/client/add/',
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-book").modal("show");
      },
      success: function (data) {
        $("#modal-book .modal-content").html(data.html_form);
      }
    });
  });
});