package com.index;

import java.util.*;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

@Configuration
@ConfigurationProperties("my")
public class Config {
	private List<String> servers = new ArrayList<String>();
	
	public List<String> getServers(){
		return this.servers;
	}

}
