package com.vdcoding.batman.mapper;

import java.util.List;

import org.apache.ibatis.annotations.Param;

import com.vdcoding.batman.pojos.Goods;

public interface GoodsMapper {
	
	Goods getGoodsById(int goodsId);
	List<Goods> getGoods(
			@Param("categoryId") int categoryId, 
			@Param("content")String content,
			@Param("from")int from, 
			@Param("limit")int limit);
}
