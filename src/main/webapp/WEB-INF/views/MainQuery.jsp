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

<script src="/lib/jquery-3.7.1.min.js"></script>
<script type="text/javascript">
$(document).ready(function() {
	
	set_Event();
	
	function set_Event() {
		$("#commit").click(function() {
			var query = $("input[name=query]").val();
			func_runQuery(query);
		});
	}
	
	function func_runQuery(query) {
		var params = {};
		params['query'] = query;
		console.log(params)
		
		$.ajax({
			url : "/main/commitQuery",
			type : "POST",			
			data : JSON.stringify(params),
			//요청 성공 시 동작할 콜백 함수 지정
			success : function(data) {
				console.log(data);
			}
		});
	}
})
</script>
</body>
</html>