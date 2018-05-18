package com.vdcoding.batman.mapper;

import java.util.HashMap;
import java.util.List;

import org.apache.ibatis.annotations.Param;

import com.vdcoding.batman.pojos.Comments;

public interface CommentsMapper {
	
	/*
	 * 接收多个参数时，需要使用Param注解标明该形参映射到sql中的哪个占位符
	 * 例如：xml文件中sql占位符为#{goods_id}，则使用@Param("goods_id")
	 * 
	 * 另一种方式是不使用Param注解，直接在sql中通过索引的方式引用参数，使用这种方式后sql中的占位符为#{0}, #{1}
	 * 索引值与传入接口方法的形参位置一一对应
	 */
	List<Comments> getComments(@Param("goodsId")int goodsId, @Param("from")int from, @Param("limit")int limit);
	
	HashMap<String, Object> getCommentsCount(int goodsId);
	
}
