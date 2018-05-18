package restapi.controller;

import java.util.List;
import java.util.Map;

import static org.springframework.web.bind.annotation.RequestMethod.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import restapi.data.BlogRepository;

@RestController
@RequestMapping("/blog")
public class BlogController {
	private BlogRepository blogDao;
	
	@Autowired
	public BlogController(BlogRepository blogDao){
		this.blogDao = blogDao;
	}
	
	@RequestMapping(value="/getpost", method=GET)
	public List<Map<String, Object>> getPopularPost(){
		return blogDao.findPopularPosts();
	}
}
