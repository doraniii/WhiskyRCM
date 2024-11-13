package com.web.whisky.data;

import java.util.List;

import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class ResponseTrans {
	
	@JsonProperty
	private List<Translation> translations;
}
