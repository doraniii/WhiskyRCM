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
			$("#whiskyInfo").toggle();
		});

		$(document).on("click","#retry", function() {
			location.reload();
		});

	}
	
	/* 쿼리를 받아서 처리하는 함수 */
	function func_runQuery(query) {
		var params = {};
		params['query'] = query;
		
		$.ajax({
			url : "/main/runQuery/commit.do",
			type : "post",	
			data : params,               
			success : function(data) {
				func_getResult(data);
				
				/* 진짜 데이터 */
				/* var review = data; 
				console.log(review) */
				
				/* API 테스트용 가짜 데이터 */
				var review = [
    				{
        				category: 'Single Malt Scotch',
        				name: 'Highland Park Harald, 40%',
        				review: 'Hi'
    				},
    				{
        				category: 'Single Malt Scotch',
        				name: 'Highland Park Sigurd, 43%',
        				review: 'Sorry'
    				}
				];
				
				$(document).on("click","#trans", function() {
					var checkEng = true;
					func_reviewTrans(checkEng, review);
				});
				
			}
		});
	}
	
	/* 결과를 Response 받아서 화면에 뿌려주는 함수 */
	function func_getResult(data) {
		var result = data.result;
		
		html = "";
		
		for (i=0; i<result.length; i++) {						
			html += "<p>" + result[i].name + "</p>";
			html += "<p>" + result[i].category + "</p>";
			html += "<p id='resultReview'>" + result[i].review + "</p>";
			html += "<hr/>";
		}
		
		html += "<button type='button' id='retry'>Retry</button>";
		html += "<button type='button' id='trans'>Translation</button>";
		
		$("#queryResult").html(html);
	}
	
	/* 리뷰를 번역해주는 함수 */
	function func_reviewTrans(checkEng, review) {
		var params = {};
		params['checkEng'] = checkEng;
		params['review'] = review;
		
		console.log(params);
		

		$.ajax({
			url : "/main/runQuery/translateReview.do",
			type : "post",	
			data : params,               
			success : function(data) {
				console.log(data);
			}
		});
		
	}
})
</script>
</body>
</html>