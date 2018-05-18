package restapi.pojo;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;


/*
 * 使用xml注解生成微信xml图文响应消息
 */
@XmlRootElement(name="xml")
public class PicTextResponse extends BaseResponse{
	@XmlElement
	private String MsgType = "news";
	@XmlElement
	private int ArticleCount;
	@XmlElement(name="Articles")
	private Article article;
	
	public PicTextResponse(){};
	public PicTextResponse(String username, String devname, List<Map<String, Object>> items){
		super(username, devname);
		this.ArticleCount = items.size();
		this.article = new Article(items);
	}
	
}

class Article{
	@XmlElement(name="item")
	private ArrayList<Item> items;
	
	public Article(List<Map<String, Object>> list){
		ArrayList<Item> temp = new ArrayList<>();
		for (Map<String, Object>item:list){
			temp.add(new Item(item));
		}
		this.items = temp;
	}
	public ArrayList<Item> getItems(){
		return items;
	}
	
}
class Item{
	@XmlElement
	private String Title;
	@XmlElement
	private String Description;
	@XmlElement
	private String PicUrl;
	@XmlElement
	private String Url;
	
	public Item(){};
	public Item(Map<String, Object> item){
		Object tempUrl = item.get("picurl");
		this.Title = item.get("post_title").toString();
		this.Description = item.get("post_title").toString();
		this.PicUrl = (tempUrl != null)?tempUrl.toString():"http://47.93.234.171/wp-content/uploads/2017/11/weixin_coding_2.jpg";
		this.Url = item.get("guid").toString();
	}
	
}
