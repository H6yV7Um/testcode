package restapi.data;

import java.util.List;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.jdbc.core.JdbcOperations;
import org.springframework.stereotype.Repository;


@Repository
public class BlogRepository implements JdbcRepository {
	/*
	 * 定义jdbctemplate时通过Bean注解显式声明bean的名称，在自动注入引用时，
	 * 通过Qualifier注解标注要引用哪个bean，这样即可实现多数据库的使用
	 */
	@Autowired
	@Qualifier("prodb")
	private JdbcOperations jdbc;
	
	@Autowired
	@Qualifier("testdb")
	private JdbcOperations testjdbc;
	
	private final Logger logger = LoggerFactory.getLogger(this.getClass());

	public List<Map<String, Object>> findPopularPosts() {
		return jdbc.queryForList(
				"SELECT DISTINCT(a.`postid`), a.`pageviews`, b.`post_title`,b.`guid`, c.picurl "
				+ "FROM wp_popularpostsdata a LEFT JOIN wp_posts b ON a.`postid`=b.`ID` "
				+ "LEFT JOIN (SELECT b.post_id, a.guid AS picurl FROM wp_posts a,"
				+ "(SELECT post_id,meta_value FROM wp_postmeta WHERE meta_key='_thumbnail_id') b "
				+ "WHERE a.id=b.meta_value) as c on b.`ID`=c.post_id WHERE b.`post_type`='post' ORDER BY a.`pageviews` DESC LIMIT 7;"
				);
	}
	
	public List<Map<String, Object>> findLatestPosts(){
		return jdbc.queryForList(
				"SELECT DISTINCT(a.`postid`), a.`pageviews`, b.`post_title`,b.`guid`, c.picurl "
				+ "FROM wp_popularpostsdata a LEFT JOIN wp_posts b ON a.`postid`=b.`ID` "
				+ "LEFT JOIN (SELECT b.post_id, a.guid AS picurl FROM wp_posts a,"
				+ "(SELECT post_id,meta_value FROM wp_postmeta WHERE meta_key='_thumbnail_id') b "
				+ "WHERE a.id=b.meta_value) as c on b.`ID`=c.post_id WHERE b.`post_type`='post' ORDER BY b.`post_date` DESC LIMIT 7;"
				);
	}

	public List<Map<String,Object>> searchPosts(String field){
		return jdbc.queryForList(
				"SELECT DISTINCT(a.`postid`), a.`pageviews`, b.`post_title`,b.`guid`, c.picurl "
				+ "FROM wp_popularpostsdata a LEFT JOIN wp_posts b ON a.`postid`=b.`ID` "
				+ "LEFT JOIN (SELECT b.post_id, a.guid AS picurl FROM wp_posts a,"
				+ "(SELECT post_id,meta_value FROM wp_postmeta WHERE meta_key='_thumbnail_id') b "
				+ "WHERE a.id=b.meta_value) AS c ON b.`ID`=c.post_id "
				+ "WHERE b.`post_type`='post' AND b.post_content LIKE CONCAT('%',?,'%') ORDER BY a.`pageviews` DESC LIMIT 7;",
				field);
	}
}
