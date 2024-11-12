<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Insert title here</title>
</head>
<body>	
	<div>
		<form name="whiskyInfo" id="whiskyInfo" method="post">
			<input type="text" name="query" placeholder="Please tell me your taste in whiskey.">
			<button type="button" id="commit">commit</button>
		</form>
	</div>
		
	<div id="queryResult">
		<span></span>
	</div>

<script src="/lib/jquery-3.7.1.min.js"></script>
<script type="text/javascript">
$(document).ready(function() {
	
	set_Event();
	
	/* 이벤트 처리 함수 */
	function set_Event() {
		$("#commit").click(function() {
			var query = $("input[name=query]").val();
			func_runQuery(query);
		});
	}
	
	/* 쿼리를 받아서 처리하는 함수 */
	function func_runQuery(query) {
		var params = {};
		params['query'] = query;
		
		$.ajax({
			url : "/main/runQuery/commit.do",
			type : "post",	
			contentType: 'application/json; charset=UTF-8', // JSON 형식으로 요청
			data : JSON.stringify(params),               
			success : function(data) {
				func_getResult(data)
			}
		});
	}
	
	/* 결과를 Response 받아서 화면에 뿌려주기 */
	function func_getResult(data) {
		var result = data.result;
		html = "";
		
		for (i=0; i<result.length; i++) {						
			html += "<p>" + result[0].name + "</p>";
			html += "<p>" + result[0].category + "</p>";
			html += "<p>" + result[0].review + "</p>";
			html += "<hr/>";
		}
		
		$("#queryResult").html(html);
	}
})
</script>
</body>
</html>