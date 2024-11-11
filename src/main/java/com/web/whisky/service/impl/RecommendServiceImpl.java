package com.web.whisky.service.impl;

import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

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
	
	@Value("${deepl.url}")
	private String deeplApiUrl;
	@Value("${deepl.key}")
    private String key;

	@Override
	public List<Map<String, Object>> runQuery(Map<String, Object> params) {
		
		/* WeaviateDB 연결 및 설정*/
		Config config = new Config("http", host + ":" + port);
		WeaviateClient client = new WeaviateClient(config);	
		
		String[] target_vector = {"review_vector"};
		
		NearTextArgument nearText = NearTextArgument.builder()
		    .concepts(new String[]{ (String) params.get("query") })
			.targetVectors(target_vector)
			.build();

		Fields fields = Fields.builder()
			.fields(new Field[]{
			Field.builder().name("name").build(),
			Field.builder().name("category").build(),
			Field.builder().name("review").build(),
			}).build();

		String query = GetBuilder.builder()
		    .className("Whisky")
		    .fields(fields)
			.withNearTextFilter(nearText)
			.limit(2)
			.build()
			.buildQuery();

		/* 쿼리 결과값을 알맞은 형태로 return */
		Result<GraphQLResponse> result = client.graphQL().raw().withQuery(query).run(); 
            ObjectMapper objectMapper = new ObjectMapper();
            JsonNode rootNode = objectMapper.valueToTree(result.getResult());
            JsonNode whiskyNode = rootNode.at("/data/Get/Whisky");
            
            List<Map<String, Object>> resultMap = objectMapper.convertValue(whiskyNode, new TypeReference<List<Map<String, Object>>>(){});
            
		return resultMap;
	}

	@Override
	public String translationReview(Map<String, Object> params) {
		// TODO Auto-generated method stub
		return null;
	}


}
