package com.web.whisky.service.impl;

import java.util.Map;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Service;

import com.web.whisky.service.RecommendService;

import io.weaviate.client.Config;
import io.weaviate.client.WeaviateClient;
import io.weaviate.client.base.Result;
import io.weaviate.client.v1.graphql.model.GraphQLResponse;
import io.weaviate.client.v1.graphql.query.argument.NearTextArgument;
import io.weaviate.client.v1.graphql.query.fields.Field;

@Service
public class RecommendServiceImpl implements RecommendService {
	
	@Value("${weaviate.host}")
	private String host;
	@Value("${weaviate.port}")
	private String port;

	@Override
	public String runQuery(Map<String, Object> params) {
		
		/* WeaviateDB 연결 및 설정*/
		Config config = new Config("http", host + ":" + port);
		WeaviateClient client = new WeaviateClient(config);	
		
		NearTextArgument nearText = client.graphQL().arguments().nearTextArgBuilder()
			      .concepts(new String[]{ (String) params.get("query") })
			      .distance(0.6f) // use .certainty(0.7f) prior to v1.14
			      .build();
		
		Field name = Field.builder().name("name").build();
	    Field _additional = Field.builder()
	      .name("_additional")
	      .fields(new Field[]{
	        Field.builder().name("certainty").build(), // only supported if distance==cosine
	        Field.builder().name("distance").build(),  // always supported
	      }).build();
	    
		Result<GraphQLResponse> result = client.graphQL().get()
			      .withClassName("whisky")
			      .withFields(name, _additional)
			      .withNearText(nearText)
			      .run();
		
		
		
		return result.getResult().toString();
	}

}
