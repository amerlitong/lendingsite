$(function () {

	/*Functions*/

	var	loadForm = function() {
		var btn = $(this);
		$.ajax({
		    url: btn.attr("data-url"),
		    type: 'get',
		    dataType: 'json',
		    beforeSend: function () {
		    	$("#modal-client").modal("show");
		    },
      		success: function (data) {
        		$("#modal-client .modal-content").html(data.html_form);
      		}
    	});
    };

    var saveForm = function(){
    	var form = $(this);
    	$ajax({
    		url: form.attr("action"),
    		data: form.serialize(),
    		type: form.attr("method"),
    		dataType: 'json',
    		success: function (data) {
    			if (data.form_is_valid) {
    				$("#table-client tbody").html(data.html_client_list);
    				location.href = "/lending/client/"
    			}
    			else {
    				$("#modal-client .modal-content").html(data.html_form);
    			}		
    		}
    	});
    	return false;
    };

    var delClient = function(){
    	var btn = $(this);
    	$ajax({
    		url: btn.attr("data-url"),
    		success: location.href = '/lending/client/'
    	});
    };

    /*Bindings*/

	$(".js-add-client").click(loadForm);
	$("#modal-client").on("submit",".js-client-form",saveForm);

	$(".js-del-client").click(delClient);

});