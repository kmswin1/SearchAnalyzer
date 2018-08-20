$( document ).ready(function() {
	$("#nav-proxy").addClass('active');

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
	var query = $("#url").val();
	var url = "proxy_view?url=" + encodeURIComponent(query);
	window.open(url, "_self", "");
}
