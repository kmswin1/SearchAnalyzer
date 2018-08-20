$( document ).ready(function() {
	var isFirst;
	if (document.location.href.split("/")[3] === "poi_search") {
		isFirst = true;
	} else {
		isFirst = false;
	}
    function init() {
        if (!isFirst) {
	        var link = document.location.href.split("=");
	        var link2 = link[2].split("&");
	        var tp = link[link.length - 1] // url 로 부터 type 값 구함
	        if (tp === "" || tp === undefined) {
	            tp = "query_type"
	            $("#type").val(tp);
	        }
	        var curLoc = link2[0].split(",");
	        /* url 로 부터 중심좌표를 구하는 과정*/
            $("#cur_center").text(curLoc[0] + ", " + curLoc[1]); //중심좌표 표시
            // 초기 화면이 아니라면 url 로 중심좌표를 구함
            if (tp !== "") {
                $("#type").val(tp);
            }
        } else {
            $("#cur_center").text("좌표설정 후 검색해주세요.");
            // 초기 화면시 설정이 안됀 상태
        }
    }

    init();


	$('#frame_1').change(function() {
        if ($("#frame_1 option:selected").val() === "T_ALLY") {
        	$("#frame_input").empty();
        	$("#frame_input").append('<input type="text" class="form-control" style="width: 60px;" id="frame_nums" value="10" />');
		} else if ($("#frame_1 option:selected").val() === "T_PRD") {
        	$("#frame_input").empty();
        	$("#frame_input").append('<input type="text" class="form-control" style="width: 60px;" id="frame_nums" value="10" />');
		} else if ($("#frame_1 option:selected").val() === "T_DEV") {
        	$("#frame_input").empty();
        	$("#frame_input").append('<input type="text" class="form-control" style="width: 60px;" id="frame_nums" value="10" />');
		} else {
        	if (($("#frame_2 option:selected").val() === "N" || $("#frame_2 option:selected").val() === "K") && ($("#frame_3 option:selected").val() === "N" || $("#frame_3 option:selected").val() === "K")) {
        		$("#frame_input").empty();
			}
		}
	});


	$('#frame_2').change(function() {
        if ($("#frame_2 option:selected").val() === "T_ALLY") {
        	$("#frame_input").empty();
        	$("#frame_input").append('<input type="text" class="form-control" style="width: 60px;" id="frame_nums" value="10" />');
		} else if ($("#frame_2 option:selected").val() === "T_PRD") {
        	$("#frame_input").empty();
        	$("#frame_input").append('<input type="text" class="form-control" style="width: 60px;" id="frame_nums" value="10" />');
		} else if ($("#frame_2 option:selected").val() === "T_DEV") {
        	$("#frame_input").empty();
        	$("#frame_input").append('<input type="text" class="form-control" style="width: 60px;" id="frame_nums" value="10" />');
		} else {
        	if (($("#frame_1 option:selected").val() === "N" || $("#frame_1 option:selected").val() === "K") && ($("#frame_3 option:selected").val() === "N" || $("#frame_3 option:selected").val() === "K")) {
        		$("#frame_input").empty();
			}
		}
	});


	$('#frame_3').change(function() {
        if ($("#frame_3 option:selected").val() === "T_ALLY") {
        	$("#frame_input").empty();
        	$("#frame_input").append('<input type="text" class="form-control" style="width: 60px;" id="frame_nums" placeholder="the number of lists" value="10" />');
		} else if ($("#frame_3 option:selected").val() === "T_PRD") {
        	$("#frame_input").empty();
        	$("#frame_input").append('<input type="text" class="form-control" style="width: 60px;" id="frame_nums" placeholder="the number of lists" value="10" />');
		} else if ($("#frame_3 option:selected").val() === "T_DEV") {
        	$("#frame_input").empty();
        	$("#frame_input").append('<input type="text" class="form-control" style="width: 60px;" id="frame_nums" placeholder="the number of lists" value="10" />');
		} else {
        	if (($("#frame_1 option:selected").val() === "N" || $("#frame_1 option:selected").val() === "K") && ($("#frame_2 option:selected").val() === "N" || $("#frame_2 option:selected").val() === "K")) {
        		$("#frame_input").empty();
			}
		}
	});

	$('#center').change(function() {
		if ($("#center option:selected").val() === "n") {
			$("#center-form").empty();
			$("#center-form").append('<input type="text" class="form-control" id="delta_x" placeholder="X좌표"/>');
			$("#center-form").append('<input type="text" class="form-control" id="delta_y" placeholder="Y좌표"/>');
		} else if ($("#center option:selected").val() === "current") {
			$("#center-form").empty();
			$("#center-form").append('<div class="well well-sm" id="cur_center"></div>');
			init();
		} else {
			$("#center-form").empty();
		}
	});

	$("#nav-search").addClass('active');


	$(document).keypress(function(e) {
		if (e.which == 13) {
			$("#searchButton").trigger('click');
			return false;
		}
	});
	$("#searchButton").click(function(e) {
		if ($("input:radio[name=sel_option]:checked").val() === "normal") {
			search("normal",isFirst,$("#type").val());
        } else {
			search("debug",isFirst,$("#type").val());
		} // radio button 에 따라서 normal , debug 다르게 검색 가능
		return false;
	});

	var radioCheck = $("#engineTypeHidden").val();
	$("input[name=engineType][value=" + radioCheck + "]").attr("checked", true);

	$('#contact').on('click', function() {
		if($(this).hasClass('selected')) {
			deselect($(this));
		} else {
			$(this).addClass('selected');
			$('.pop').slideFadeToggle();
		}
		return false;
	});

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

	$('.search_view_close').on('click', function() {
		view_deselect($('#search_view'));
		return false;
	});



	var nluYn = $("#nluHidden").val();
	if (nluYn == "y") {
		$("input[name=nlu]").attr("checked", true);
	}

	var dupYn = $("#dupHidden").val();
	if (dupYn == "y") {
		$("input[name=dup]").attr("checked", true);
	}

	$('a.page').on('click', function() {
		alert("1");
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
// the end of document.getReady

function search(search_type, isFirst, type) {
    var rows;
    if ($("#frame_1 option:selected").val() === "T_ALLY") {
        rows = $("#frame_nums").val();
    } else if ($("#frame_1 option:selected").val() === "T_PRD") {
        rows = $("#frame_nums").val();
    } else if ($("#frame_1 option:selected").val() === "T_DEV") {
        rows = $("#frame_nums").val();
    }
    if ($("#frame_2 option:selected").val() === "T_ALLY") {
        rows = $("#frame_nums").val();
    } else if ($("#frame_2 option:selected").val() === "T_PRD") {
        rows = $("#frame_nums").val();
    } else if ($("#frame_2 option:selected").val() === "T_DEV") {
        rows = $("#frame_nums").val();
    }
    if ($("#frame_3 option:selected").val() === "T_ALLY") {
        rows = $("#frame_nums").val();
    } else if ($("#frame_3 option:selected").val() === "T_PRD") {
        rows = $("#frame_nums").val();
    } else if ($("#frame_3 option:selected").val() === "T_DEV") {
        rows = $("#frame_nums").val();
    }

	var query = $("#searchQuery").val();

	var search_center = $("#center option:selected").val();

	if (type === "" || type === undefined) {
	    type = "query_type";
	}
	if (search_center === "n") {
        search_center = $("#delta_x").val() + "," + $("#delta_y").val();
        // 직접 입력 선택 시 입력 값 받아옵니다.
    } else if (search_center === "current") {
		if (isFirst) {
			search_center = "4571671,1352269";
        } else {
			var link = document.location.href.split("=");
			var link2 = link[2].split("&");
			var curLoc = link2[0].split(",");
			/* url 로 부터 중심좌표를 구하는 과정*/
			search_center = curLoc[0] + "," + curLoc[1];
		}
	}

	var frame_1 = $("#frame_1 option:selected").val();
	var frame_2 = $("#frame_2 option:selected").val();
	var frame_3 = $("#frame_3 option:selected").val();

	var url = "poi_search?q=" + encodeURIComponent(query)
		+ "&center=" + search_center
        + "&rows=" + rows
		+ "&search_type=" + search_type
		+ "&frame_1=" + frame_1
		+ "&frame_2=" + frame_2
		+ "&frame_3=" + frame_3
		+ "&type=" + type;
	window.open(url, "_self", "");
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
