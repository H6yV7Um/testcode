package com.vdcoding;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.boot.web.support.SpringBootServletInitializer;
import org.springframework.context.annotation.Import;

import com.vdcoding.datasources.DynamicDataSourceConfig;


@SpringBootApplication(exclude={DataSourceAutoConfiguration.class})
@Import({DynamicDataSourceConfig.class})
public class LeagueApplication extends SpringBootServletInitializer {

	public static void main(String[] args) {
		SpringApplication.run(LeagueApplication.class, args);
	}

	@Override
	protected SpringApplicationBuilder configure(SpringApplicationBuilder application) {
		return application.sources(LeagueApplication.class);
	}
}
