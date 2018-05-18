package com.index;

import java.util.*;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@EnableAutoConfiguration
public class Entry {
	
	@RequestMapping("/")
	String home(){
		return "Hello Spring Boot";
	}
	
	@RequestMapping("/sub")
	List<String> subpage(){
		Config config = new Config();
		List<String> servers = config.getServers();
		return servers;
	}
	
	@RequestMapping("/float")
	float floatpage(){
		return (float) 3.14;
	}
	
	public static void main(String[] args) throws Exception {
		SpringApplication.run(Entry.class, args);
	}
}
