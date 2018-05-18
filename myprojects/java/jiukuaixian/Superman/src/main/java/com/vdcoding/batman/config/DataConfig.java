package com.vdcoding.batman.config;


import javax.sql.DataSource;

import org.apache.commons.dbcp.BasicDataSource;
import org.mybatis.spring.SqlSessionFactoryBean;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.context.annotation.PropertySource;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.core.env.Environment;
import org.springframework.core.io.ClassPathResource;


@Configuration
@PropertySource("classpath:db.properties")
public class DataConfig {
	@Autowired
	Environment env;
	
	@Primary
	@Bean(name="proDbConfig")
	@ConfigurationProperties(prefix="test.jdbc")
	public DataSource dataSource(){
		/*
		 * 通过ConfigurationProperties注解的方式获取db.properties中前缀为test.jdbc的属性值，并自动调用setter为DataSource赋值
		 * 所以db.properties中数据库配置名称要与DataSource的setter方法匹配上
		 * 例如：setter方法为ds.setDriverClassName，则db.properties中设置的配置名称为test.jdbc.driver-class-name 或者
		 * 以驼峰方式命名也可以test.jdbc.driverClassName
		 */
		return new BasicDataSource();
	}
	
	@Bean(name="testDbConfig")
	public DataSource testDataSource(){
		/*
		 * 在配置类上使用@PropertySource注解后，会自动将db.properties添加到spring的Environment环境变量中
		 */
		BasicDataSource ds = new BasicDataSource();
		ds.setDriverClassName(env.getProperty("test.jdbc.driverClassName", "com.mysql.jdbc.Driver"));
		ds.setUrl(env.getProperty("test.jdbc.url"));
		ds.setUsername(env.getProperty("test.jdbc.username"));
		ds.setPassword(env.getProperty("test.jdbc.password"));
		ds.setInitialSize(2);
		ds.setMaxActive(1);
		ds.setTestOnBorrow(true);
		ds.setValidationQuery("select 1");
		return ds;
	}
	
	@Primary
	@Bean(name="prodb")
	public JdbcTemplate jdbcTemplate(@Qualifier("proDbConfig") DataSource prods){
		return new JdbcTemplate(prods);
	}
	@Bean(name="testdb")
	public JdbcTemplate testJdbcTemplate(@Qualifier("testDbConfig") DataSource testds){
		return new JdbcTemplate(testds);
	}
	
	@Bean(name="sessionFactory")
	public SqlSessionFactoryBean sqlSessionFactoryBean(@Qualifier("testDbConfig") DataSource prods){
		SqlSessionFactoryBean factory = new SqlSessionFactoryBean();
		factory.setConfigLocation(new ClassPathResource("mybatis-config.xml"));
		factory.setDataSource(prods);
//		factory.setEnvironment("production");
		return factory;
	}
	
}
