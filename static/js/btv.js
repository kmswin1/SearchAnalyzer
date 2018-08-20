$( document ).ready(function() {
	$("#nav-btv").addClass('active');

	$(document).keypress(function(e) {
		if (e.which == 13) {
			$("#searchNewsButton").trigger('click');
			return false;
		}
	});

	$("#searchNewsButton").click(function(e) {
		searchNews();
		return false;
	});
	$('#contact').on('click', function() {
		if($(this).hasClass('selected')) {
			deselect($(this));			   
		} else {
			$(this).addClass('selected');
			$('.pop').slideFadeToggle();
		}
		return false;
	});

	var nluYn = $("#nluHidden").val();
	if (nluYn == "y") {
		$("input[name=nlu]").attr("checked", true);
	}
	
	var nowTimeYn = $("#nowTimeHidden").val();
	if (nowTimeYn == "y") {
		$("input[name=now_time]").attr("checked", true);
		$("input[name=setSearchTime]").attr('disabled','disabled');
	}
	$('.pop_close').on('click', function() {
		deselect($('#contact'));
		return false;
	});

	$('#search_view').on('click', function() {
		if($(this).hasClass('selected')) {
			view_deselect($(this));			   
		} else {
			$(this).addClass('selected');
			$('.search_view_pop').slideFadeToggle();
		}
		return false;
	});

	$("input[name=now_time]").click(function() {
		if ($("input[name=setSearchTime]")[0].hasAttribute('disabled') == true) {
			$("input[name=setSearchTime]").removeAttr('disabled');
		} else {
			$("input[name=setSearchTime]").attr('disabled','disabled');
		}
	});

	$('.search_view_close').on('click', function() {
		view_deselect($('#search_view'));
		return false;
	});

	$(document).mousedown(function(e){
		$("#query_pop").each(function() {
			if ($("#search_view").hasClass('selected')) {
				var l_position = $("#query_pop").offset();
					l_position.right = parseInt(l_position.left) + ($("#query_pop").width());
				l_position.bottom = parseInt(l_position.top) + parseInt($("#query_pop").height());
				if( ( l_position.left <= e.pageX && e.pageX <= l_position.right ) && ( l_position.top <= e.pageY && e.pageY <= l_position.bottom ) ) {
				} else {
					view_deselect($('#search_view'));
				}
			}
		});
	});

	$('a[name="explanation"]').click(function(){
		var $href = $(this).attr('idhref');
		layer_popup($href);
	});

	$(".dropdown-menu li a").click(function(){
  		var selText = $(this).text();
  		$(this).parents('.dropdown').find('.dropdown-toggle').html(selText+' <span class="caret"></span>');
		var index = selected_index = $(this).closest('li').index();
		SEARCH_TYPE = index;
	});	

	function layer_popup(el){
		var $el = $(el);
		$el.fadeIn();

		var $elWidth = ~~($el.outerWidth()),
			$elHeight = ~~($el.outerHeight()),
			docWidth = $(document).width(),
			docHeight = $(document).height();
		$el.css({top: 0, left: 0});

		$el.find('a.btn-layerClose').click(function(){
			$el.fadeOut(); 
			return false;
		});
	}
});

function searchNews() {
	var query = document.getElementById('searchNewsQuery').value;
	var set_search_time = document.getElementById('setSearchTime').value;

	var nlu_yn = "";
	$("input[name=nlu]:checked").each(function() {
		nlu_yn = $(this).val();
	});

	var now_time_yn = "";
	$("input[name=now_time]:checked").each(function() {
		now_time_yn = $(this).val();
	});

	var url = "btv_search?q=" + encodeURIComponent(query) + "&nlu_yn=" + nlu_yn + "&now_time_yn=" + now_time_yn + "&set_search_time=" + set_search_time;
	console.log(url);
	window.open(url, "_self", "");

	return true;
}

function deselect(e) {
	$('.pop').slideFadeToggle(function() {
		e.removeClass('selected');
	});
}

function view_deselect(e) {
	$('.search_view_pop').slideFadeToggle(function() {
		e.removeClass('selected');
	});
}

$.fn.slideFadeToggle = function(easing, callback) {
	return this.animate({ opacity: 'toggle', height: 'toggle' }, 'fast', easing, callback);
};
