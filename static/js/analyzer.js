$( document ).ready(function() {
	$("#nav-analyzer").addClass('active');

	var search_view_open = false;
	var contact_open = false;
	$(document).keypress(function(e) {
		if (e.which == 13) {
			$("#searchButton").trigger('click');
			return false;
		}
	});
	$("#searchButton").click(function(e) {
		search();
		return false;
	});
});

function search() {
	var query = $("#text").val();
	var url = "analyzer?text=" + encodeURIComponent(query);
	window.open(url, "_self", "");
}
