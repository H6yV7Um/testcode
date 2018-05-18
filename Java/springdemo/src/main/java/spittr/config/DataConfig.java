package spittr.config;

import javax.sql.DataSource;
import org.apache.commons.dbcp.BasicDataSource;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
//import org.springframework.context.annotation.Profile;
//import org.springframework.jdbc.core.JdbcOperations;
import org.springframework.jdbc.core.JdbcTemplate;
//import org.springframework.jdbc.datasource.embedded.EmbeddedDatabaseBuilder;
//import org.springframework.jdbc.datasource.embedded.EmbeddedDatabaseType;

@Configuration
public class DataConfig {
  
//  @Profile("demo")
//  @Bean
//  public DataSource dataSource() {
//    return new EmbeddedDatabaseBuilder()
//            .setType(EmbeddedDatabaseType.H2)
//            .addScript("classpath:schema.sql")
//            .build();
//  }
  
//  @Profile("qatest")
  @Bean
  public DataSource testDataSource(){
	  BasicDataSource ds = new BasicDataSource();
	  ds.setDriverClassName("com.mysql.jdbc.Driver");
	  ds.setUrl("jdbc:mysql://172.16.16.72:3306/test?useUnicode=true&characterEncoding=UTF-8");
	  ds.setUsername("svcload");
	  ds.setPassword("51talk");
	  ds.setInitialSize(10);
	  ds.setMaxActive(10);
	  return ds;
  }
  
  @Bean
  public JdbcTemplate jdbcTemplate(DataSource dataSource) {
    return new JdbcTemplate(dataSource);
  }
  

}
