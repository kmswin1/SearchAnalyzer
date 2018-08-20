$( document ).ready(function() {

    $('#hostSubmit').click(function() {
        var hostname = $("#host").val();
        var hostinfo = $("#hostInfo").val();
        var encoding;
        var doctype;
        if (hostname === "" || hostinfo === "") {
            alert("호스트명이나 호스트설명을 입력해 주세요.")
            return;
        }
        if ($("input:radio[name=encoding_type]:checked").val() === "utf-8") {
            encoding = "utf-8";
        } else if ($("input:radio[name=encoding_type]:checked").val() === "euc-kr") {
            encoding = "euc-kr";
        }

		if ($("input:radio[name=doc_type]:checked").val() === "json") {
            doctype = "json";
        } else if ($("input:radio[name=doc_type]:checked").val() === "xml") {
            doctype = "xml";
		} else if ($("input:radio[name=doc_type]:checked").val() === "html") {
            doctype = "html";
        }

        json_data = JSON.stringify({
            hostname: hostname,
            hostinfo: hostinfo,
            encoding: encoding,
            doctype: doctype
        });
        $.ajax({
            type: 'POST',
            url: '/addHost',
            contentType: 'application/json; charset=utf-8',
            traditional: true,
            async: false,
            data: json_data,
            success: function (data) {
                console.log(data);
            },
            error: function (xhr) {
                console.log (data);
            }
        });
        $.ajax({
            type: 'GET',
            url: '/addHost',
            traditional: true,
            async: false,
            data: {},
            success: function (data) {
                window.location.reload()
            },
            error: function (xhr) {
                console.log (data);
            }
        });
    }); // 호스트 등록 버튼 클릭 시


    $('#keywordSubmit').click(function() {
        var tempname = $("#keywordFile").val().split("\\");
        var keywordname = tempname[tempname.length-1];
        var keywordinfo = $("#keywordInfo").val();
        if (keywordinfo === "") {
            alert("검색어설명을 입력해 주세요.")
            return;
        }
        json_data = JSON.stringify({
            keywordname: keywordname,
            keywordinfo: keywordinfo,
        });
        $.ajax({
            type: 'POST',
            url: '/addKeyword',
            contentType: 'application/json; charset=utf-8',
            traditional: true,
            async: false,
            data: json_data,
            success: function (data) {
                console.log(data);
            },
            error: function (xhr) {
                console.log (data);
            }
        });
        $.ajax({
            type: 'GET',
            url: '/addKeyword',
            traditional: true,
            async: false,
            data: {},
            success: function (data) {
                console.log(data)
            },
            error: function (xhr) {
                console.log (data);
            }
        });
        $("#keywordForm").submit();
    }); // 검색어 등록 버튼 클릭 시

    $("#getResultSubmit").click(function() {
        var getPath = "";
        var getKeyword = "";
        var workName = "";
        var encoding = "";
        var jsonpath = "";
        var basicQuery = $("#query").val();
        var repeatQuery = $("#repeatQuery").val();
        if ($("#hostlist option:selected").val() === "self") {
           getPath = $("#getPath").val();
        } else {
           getPath = $("#hostlist option:selected").val();
        }
        getKeyword = $("#keywordlist option:selected").val();
        workName = $("#workingName").val();
        jsonpath = $("#get_json_path").val();
        if (getPath === "" || getKeyword === "" || workName === "" || basicQuery === ""
        || repeatQuery === "") {
            alert ("추출경로, 키워드, 기본쿼리, 반복쿼리, 작업이름 중 하나가 입력되지 않았습니다.");
            return;
        }
        if ($("input:radio[name=result_encoding_type]:checked").val() === "utf-8") {
            encoding = "utf-8";
        } else if ($("input:radio[name=result_encoding_type]:checked").val() === "euc-kr") {
            encoding = "euc-kr";
        }
        workName = workName+".json";
        json_data = JSON.stringify({
            hostid : getPath,
            keywordid : getKeyword,
            resultname : workName,
            encoding : encoding,
            jsonpath : jsonpath,
            basicquery: basicQuery,
            repeatquery: repeatQuery
        });
        $.ajax({
            type: 'POST',
            url: '/getResult',
            contentType: 'application/json; charset=utf-8',
            traditional: true,
            async: false,
            data: json_data,
            success: function (data) {
                console.log(data);
            },
            error: function (xhr) {
                console.log (data);
            }
        });
        $.ajax({
            type: 'GET',
            url: '/getResult',
            traditional: true,
            async: false,
            data: {},
            success: function (data) {
                window.location.reload();
            },
            error: function (xhr) {
                console.log (data);
            }
        });
    }); // 결과 추출 버튼 클릭 시

    $("#compareResultSubmit").click(function() {
        var first_getPath = "";
        var getKeyword = "";
        var first_encoding = "";
        var first_jsonpath = $("#first_json_path").val();
        var first_basicQuery = $("#first_query").val();
        var first_repeatQuery = $("#first_repeatQuery").val();
        var second_getPath = "";
        var second_encoding = "";
        var second_basicQuery = $("#second_query").val();
        var second_repeatQuery = $("#second_repeatQuery").val();
        var workName = $("#compare_workingName").val();
        if ($("#first_hostlist option:selected").val() === "self") {
           first_getPath = $("#first_getPath").val();
        } else {
           first_getPath = $("#first_hostlist option:selected").val();
        }
        getKeyword = $("#compare_keywordlist option:selected").val();

        if ($("input:radio[name=first_encoding_type]:checked").val() === "utf-8") {
            first_encoding = "utf-8";
        } else if ($("input:radio[name=first_encoding_type]:checked").val() === "euc-kr") {
            first_encoding = "euc-kr";
        }

        if ($("#second_hostlist option:selected").val() === "self") {
           second_getPath = $("#second_getPath").val();
        } else {
           second_getPath = $("#second_hostlist option:selected").val();
        }

        if ($("input:radio[name=second_encoding_type]:checked").val() === "utf-8") {
            second_encoding = "utf-8";
        } else if ($("input:radio[name=second_encoding_type]:checked").val() === "euc-kr") {
            second_encoding = "euc-kr";
        }

        if (first_getPath === "" || workName === "" || first_basicQuery === ""
        || first_repeatQuery === "" || second_getPath === "" || getKeyword === "" || second_basicQuery === ""
        || second_repeatQuery === "") {
            alert ("추출경로, 키워드, 기본쿼리, 반복쿼리, 작업이름 중 하나가 입력되지 않았습니다.");
            return;
        }
        workName = workName+".json";
        var encoding = first_encoding;
        json_data = JSON.stringify({
            firsthostid : first_getPath,
            keywordid : getKeyword,
            resultname : workName,
            encoding : encoding,
            jsonpath : first_jsonpath,
            firstbasicquery: first_basicQuery,
            firstrepeatquery: first_repeatQuery,
            secondhostid : second_getPath,
            secondbasicquery: second_basicQuery,
            secondrepeatquery: second_repeatQuery
        });
        $.ajax({
            type: 'POST',
            url: '/compareResult',
            contentType: 'application/json; charset=utf-8',
            traditional: true,
            async: false,
            data: json_data,
            success: function (data) {
                console.log(data);
            },
            error: function (xhr) {
                console.log (data);
            }
        });
        $.ajax({
            type: 'GET',
            url: '/compareResult',
            traditional: true,
            async: false,
            data: {},
            success: function (data) {
                window.location.reload();
            },
            error: function (xhr) {
                console.log (data);
            }
        });
    }); // 결과 비교 버튼 클릭 시

});

function delHost(id) {
    json_data = JSON.stringify({
        id: id
    });
    $.ajax({
        type: 'DELETE',
        url: '/addHost',
        traditional: true,
        async: false,
        data: json_data,
        success: function (data) {
            window.location.reload();
        },
        error: function (xhr) {
            console.log (data);
        }
        });
} // 호스트 삭제 기능

function delKeyword(id) {
    json_data = JSON.stringify({
        id: id
    });
    $.ajax({
        type: 'DELETE',
        url: '/addKeyword',
        traditional: true,
        async: false,
        data: json_data,
        success: function (data) {
            window.location.reload();
        },
        error: function (xhr) {
            console.log (data);
        }
        });
} // 검색어 삭제 기능

function delResult(id) {
    json_data = JSON.stringify({
        id: id
    });
    $.ajax({
        type: 'DELETE',
        url: '/admin',
        traditional: true,
        async: false,
        data: json_data,
        success: function (data) {
            window.location.reload();
        },
        error: function (xhr) {
            console.log (data);
        }
        });
} // 결과물 삭제 기능

function openResult(id) {
    json_data = JSON.stringify({
       resultbody: id
    });
    $.ajax({
        type: 'PUT',
        url: '/admin',
        traditional: true,
        async: false,
        data: json_data,
        success: function (data) {
            jswin = window.open("", "jswin","")
            jswin.document.write(data)
        },
        error: function (xhr) {
            console.log (data);
        }
    });
} // 결과물 켜기
