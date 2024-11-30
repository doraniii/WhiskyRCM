package com.web.whisky.service.impl;

import java.net.URI;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.web.whisky.service.RecommendService;

import io.weaviate.client.Config;
import io.weaviate.client.WeaviateClient;
import io.weaviate.client.base.Result;
import io.weaviate.client.v1.graphql.model.GraphQLResponse;
import io.weaviate.client.v1.graphql.query.argument.NearTextArgument;
import io.weaviate.client.v1.graphql.query.builder.GetBuilder;
import io.weaviate.client.v1.graphql.query.fields.Field;
import io.weaviate.client.v1.graphql.query.fields.Fields;

@Service
public class RecommendServiceImpl implements RecommendService {

	@Value("${weaviate.host}")
	private String host;
	@Value("${weaviate.port}")
	private String port;

	@Override
	public List<Map<String, Object>> runQuery(Map<String, Object> params) {

		/* WeaviateDB 연결 및 설정 */
		Config config = new Config("http", host + ":" + port);
		WeaviateClient client = new WeaviateClient(config);

		String[] target_vector = { "review_vector" };

		NearTextArgument nearText = NearTextArgument.builder().concepts(new String[] { (String) params.get("query") })
				.targetVectors(target_vector).build();

		Fields fields = Fields.builder().fields(new Field[] { Field.builder().name("name").build(),
				Field.builder().name("category").build(), Field.builder().name("review").build(), }).build();

		String query = GetBuilder.builder().className("Whisky").fields(fields).withNearTextFilter(nearText).limit(2)
				.build().buildQuery();

		/* 쿼리 결과값을 알맞은 형태로 return */
		Result<GraphQLResponse> result = client.graphQL().raw().withQuery(query).run();
		ObjectMapper objectMapper = new ObjectMapper();
		JsonNode rootNode = objectMapper.valueToTree(result.getResult());
		JsonNode whiskyNode = rootNode.at("/data/Get/Whisky");

		List<Map<String, Object>> resultMap = objectMapper.convertValue(whiskyNode,
				new TypeReference<List<Map<String, Object>>>() {});

		return resultMap;
	}

	@Override
	public String translateReview(Map<String, Object> params) {
		// 제일 먼저 기존 review 값을 캐시 데이터로

		/*
		 * String review = params.get("review[review]").toString(); String targetLang =
		 * "KO"; String apiUrl = deeplApiUrl + "?target_lang=" + targetLang;
		 * 
		 * RestTemplate restTemplate = new RestTemplate();
		 * 
		 * HttpHeaders headers = new HttpHeaders();
		 * headers.setAccept(Collections.singletonList(MediaType.APPLICATION_JSON));
		 * headers.setContentType(MediaType.APPLICATION_JSON);
		 * headers.add("Authorization", "DeepL-Auth-Key " + key);
		 * 
		 * Map<String, Object> requestBody = new HashMap<>(); requestBody.put("text",
		 * new String[]{ review }); requestBody.put("target_lang", targetLang);
		 * 
		 * HttpEntity<Map<String, Object>> entity = new HttpEntity<>(requestBody,
		 * headers); ResponseTrans response = restTemplate.postForObject(apiUrl, entity,
		 * ResponseTrans.class);
		 * 
		 * ObjectMapper objectMapper = new ObjectMapper(); JsonNode root =
		 * objectMapper.readTree(response); JsonNode root2 =
		 * objectMapper.valueToTree(response);
		 * 
		 * return root2.toString();
		 */
		return null;
	}

}
