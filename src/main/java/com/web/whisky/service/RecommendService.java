package com.web.whisky.service;

import java.util.List;
import java.util.Map;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestBody;

import com.web.whisky.data.RequestTrans;
import com.web.whisky.data.ResponseTrans;

public interface RecommendService {

	public List<Map<String, Object>> runQuery(Map<String, Object> params);
	
	public String translateReview(Map<String, Object> params);	

}
