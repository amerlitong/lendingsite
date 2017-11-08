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

$("#modal-book").on("submit", ".js-add-client-form", function () {
var form = $(this);
$.ajax({
  url: form.attr("action"),
  data: form.serialize(),
  type: form.attr("method"),
  dataType: 'json',
  success: function (data) {
    if (data.form_is_valid) {
      location.href = '/lending/client/'
    }
    else {
      $("#modal-book .modal-content").html(data.html_form);
    }
  }
});
return false;
});