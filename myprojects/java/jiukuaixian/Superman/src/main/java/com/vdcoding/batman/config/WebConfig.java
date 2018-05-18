package com.vdcoding.batman.config;

import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.List;

import org.apache.log4j.xml.DOMConfigurator;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.MediaType;
import org.springframework.http.converter.HttpMessageConverter;
import org.springframework.web.servlet.ViewResolver;
import org.springframework.web.servlet.config.annotation.DefaultServletHandlerConfigurer;
import org.springframework.web.servlet.config.annotation.EnableWebMvc;
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurationSupport;
import org.springframework.web.servlet.view.InternalResourceViewResolver;

import com.alibaba.fastjson.support.config.FastJsonConfig;
import com.alibaba.fastjson.support.spring.FastJsonHttpMessageConverter;


/*
 * 相当于web.xml，声明的jsp解析器、log4j日志配置，在默认的HttpMessageConverter添加阿里的fastjson，提高对json
 * 的解析转化速度。
 */
@Configuration
//@EnableWebMvc
public class WebConfig extends WebMvcConfigurationSupport {
	/*
	 * 也可以通过实现WebMvcConfigurer接口来构造WebConfig类，这也是官方推荐做法
	 * 最开始是通过继承WebMvcConfigurerAdapter来实现的WebConfig，但是Spring5.0以上已经废弃该父类
	 */
  @Bean
  public ViewResolver viewResolver() {
    InternalResourceViewResolver resolver = new InternalResourceViewResolver();
    resolver.setPrefix("/WEB-INF/resources/");
    resolver.setSuffix(".html");
    return resolver;
  }
  
  @Override
  public void configureDefaultServletHandling(DefaultServletHandlerConfigurer configurer) {
	DOMConfigurator.configure("classpath:log4j.xml");
    configurer.enable();
    
  }
  
  @Override
  public void configureMessageConverters(List<HttpMessageConverter<?>> converters) {
      FastJsonHttpMessageConverter fastJsonConverter = new FastJsonHttpMessageConverter();
      //fastJson1.2.28版本以后需要手动设置MIME类型，否则默认为*,返回时会报错
      List<MediaType> supportedMediaTypes = new ArrayList<>();
      supportedMediaTypes.add(MediaType.APPLICATION_JSON);
      supportedMediaTypes.add(MediaType.APPLICATION_JSON_UTF8);
      supportedMediaTypes.add(MediaType.APPLICATION_ATOM_XML);
      supportedMediaTypes.add(MediaType.APPLICATION_FORM_URLENCODED);
      supportedMediaTypes.add(MediaType.APPLICATION_OCTET_STREAM);
      supportedMediaTypes.add(MediaType.APPLICATION_PDF);
      supportedMediaTypes.add(MediaType.APPLICATION_RSS_XML);
      supportedMediaTypes.add(MediaType.APPLICATION_XHTML_XML);
      supportedMediaTypes.add(MediaType.APPLICATION_XML);
      supportedMediaTypes.add(MediaType.IMAGE_GIF);
      supportedMediaTypes.add(MediaType.IMAGE_JPEG);
      supportedMediaTypes.add(MediaType.IMAGE_PNG);
      supportedMediaTypes.add(MediaType.TEXT_EVENT_STREAM);
      supportedMediaTypes.add(MediaType.TEXT_HTML);
      supportedMediaTypes.add(MediaType.TEXT_MARKDOWN);
      supportedMediaTypes.add(MediaType.TEXT_PLAIN);
      supportedMediaTypes.add(MediaType.TEXT_XML);
      fastJsonConverter.setSupportedMediaTypes(supportedMediaTypes);
      converters.add(fastJsonConverter);
  }
  
  @Override
  public void addResourceHandlers(ResourceHandlerRegistry registry) {
    // TODO Auto-generated method stub
	registry.addResourceHandler("swagger-ui.html")
      		.addResourceLocations("classpath:/META-INF/resources/");

    registry.addResourceHandler("/webjars/**")
      		.addResourceLocations("classpath:/META-INF/resources/webjars/");
    super.addResourceHandlers(registry);
  }
  

}
