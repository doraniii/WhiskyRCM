package com.web.whisky.data;

import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class Translation {
	
	@JsonProperty
	private String detected_source_language;
	@JsonProperty
    private String text;
}
