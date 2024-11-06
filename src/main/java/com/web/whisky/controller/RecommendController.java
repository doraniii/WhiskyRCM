package com.web.whisky.controller;

import java.util.List;
import java.util.Map;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;

import io.weaviate.client.Config;
import io.weaviate.client.WeaviateClient;
import io.weaviate.client.base.Result;
import io.weaviate.client.v1.graphql.model.GraphQLResponse;
import io.weaviate.client.v1.graphql.query.argument.NearTextArgument;
import io.weaviate.client.v1.graphql.query.fields.Field;
import io.weaviate.client.v1.misc.model.Meta;

@Controller
public class RecommendController {

	/* 메인화면 */
	@GetMapping("/")
	public String mainPage() {
		return "MainQuery";
	}

	/* 쿼리를 받아와서 WeaviateDB에 던지기*/
	@PostMapping("/main/commitQuery")
	public String commitQuery(Map<String, Object> params) {
				
		Config config = new Config("http", "172.19.0.4:8080");
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
		
		return result.toString();
	}
	
}
