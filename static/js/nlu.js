$( document ).ready(function() {
	$("#nav-nlu").addClass('active');

	var search_view_open = false;
	var contact_open = false;
	$(document).keypress(function(e) {
		if (e.which == 13) {
			$("#searchButton").trigger('click');
			return false;

		}
	});

	var radioCheck = $("#nluTypeHidden").val();
	$("input[name=nluType][value=" + radioCheck + "]").attr("checked", true);

	$("#searchButton").click(function(e) {
		search();
		return false;
	});
});

function search() {
	var query = $("#text").val();
	var nlu_type = "";
	$("input[name=nluType]:checked").each(function() {
		nlu_type = $(this).val();
	});
	var url = "nlu?text=" + encodeURIComponent(query) + "&nlu_type=" + nlu_type;

	window.open(url, "_self", "");
}
