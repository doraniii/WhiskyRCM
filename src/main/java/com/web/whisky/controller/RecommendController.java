package com.web.whisky.controller;

import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import com.web.whisky.service.RecommendService;

@Controller
public class RecommendController {
	
	private RecommendService recommendService;
	
	@Autowired
	public RecommendController(RecommendService recommendService) {
		this.recommendService = recommendService;
	}

	/* 메인화면 */
	@GetMapping("/")
	public String mainPage() {
		return "MainQuery";
	}

	/* 쿼리를 받아와서 WeaviateDB에 던지기*/
	@PostMapping("/main/runQuery")
	public String runQuery(@RequestParam Map<String, Object> params) {		
		String result = recommendService.runQuery(params);
		return result.toString();
	}
	
}
