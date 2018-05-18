package com.vdcoding.batman.controller;

import java.util.List;


import static org.springframework.web.bind.annotation.RequestMethod.GET;
import static org.springframework.web.bind.annotation.RequestMethod.POST;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.hateoas.hal.Jackson2HalModule.TrueOnlyBooleanSerializer;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.vdcoding.batman.common.BaseResponse;
import com.vdcoding.batman.common.ResponseFactory;
import com.vdcoding.batman.common.ResponseType;
import com.vdcoding.batman.dao.GoodsDao;
import com.vdcoding.batman.pojos.Goods;

import io.swagger.annotations.Api;
import io.swagger.annotations.ApiImplicitParam;
import io.swagger.annotations.ApiOperation;

@Api(tags="商品相关接口")
@RestController
@RequestMapping("/customer/goods")
public class GoodsController {
	
	@Autowired
	private GoodsDao goodsDao;

	private final Logger logger = LoggerFactory.getLogger(this.getClass());
	
	@ApiOperation("获取商品列表")
	@RequestMapping(value="/list", method=GET)
	public BaseResponse getGoodsList(
			@RequestParam(name="category_id", defaultValue="0")int cid,
			@RequestParam(name="content", required=false)String content,
			@RequestParam("from")int from,
			@RequestParam("limit")int limit){
		
		List<Goods> goods = goodsDao.getGoods(cid, content, from, limit);
		return new BaseResponse(goods);
	}
	
	@ApiOperation("获取商品信息")
	@ApiImplicitParam(name="goodId", value="商品ID", required=true, dataType="int")
	@RequestMapping(value="/{goodsId}", method=GET)
	public BaseResponse getGoods(@PathVariable int goodsId){
		BaseResponse response;
		try {
			Goods goods = goodsDao.getGoodsById(goodsId);
			if(goods == null){
				response = ResponseFactory.getResponse(ResponseType.GOODSID_NOT_EXSIT);
			}
			else{
				response = new BaseResponse(goods);
			}
		} catch (Exception e) {
			response = ResponseFactory.getResponse(e.getMessage());
		}
		//返回String时，中文有乱码，需要重写spring默认的HttpMessageConventer，比较麻烦
//		return JSON.toJSONString(response);
		return response;
		
	}
	
}
