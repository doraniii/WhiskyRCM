package com.web.whisky.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class RecommendController {

	@GetMapping("/")
	public String test() {
		return "MainQuery";
	}

}
