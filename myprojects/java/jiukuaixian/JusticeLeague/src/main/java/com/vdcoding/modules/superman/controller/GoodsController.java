package com.vdcoding.modules.superman.controller;

import java.util.List;

import static org.springframework.web.bind.annotation.RequestMethod.GET;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.vdcoding.modules.superman.common.BaseResponse;
import com.vdcoding.modules.superman.common.ResponseFactory;
import com.vdcoding.modules.superman.common.ResponseType;
import com.vdcoding.modules.superman.pojos.Goods;
import com.vdcoding.modules.superman.pojos.GoodsCategory;
import com.vdcoding.modules.superman.service.GoodsCategoryService;
import com.vdcoding.modules.superman.service.GoodsService;

import io.swagger.annotations.Api;
import io.swagger.annotations.ApiImplicitParam;
import io.swagger.annotations.ApiOperation;


@Api(tags="商品相关接口")
@RestController
@RequestMapping("/customer/goods")
public class GoodsController {
	
	@Autowired
	private GoodsService goodsService;
	
	@Autowired
	private GoodsCategoryService goodsCategoryService;

	private final Logger logger = LoggerFactory.getLogger(this.getClass());
	
	@ApiOperation("获取商品列表")
	@RequestMapping(value="/list", method=GET)
	public BaseResponse getGoodsList(
			@RequestParam(name="category_id", defaultValue="0")int cid,
			@RequestParam(name="content", required=false)String content,
			@RequestParam("from")int from,
			@RequestParam("limit")int limit){
		
		List<Goods> goods = goodsService.getGoods(cid, content, from, limit);
		return new BaseResponse(goods);
	}
	
	@ApiOperation("获取商品信息")
	@ApiImplicitParam(name="goodId", value="商品ID", required=true, dataType="int")
	@RequestMapping(value="/{goodsId}", method=GET)
	public BaseResponse getGoods(@PathVariable int goodsId){
		BaseResponse response;
		try {
			Goods goods = goodsService.getGoodsById(goodsId);
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
	
	@GetMapping(path="/category")
	public BaseResponse getGoodsCategory(@RequestParam(name="shop_id", defaultValue="3")int shopId){
		List<GoodsCategory> categories = goodsCategoryService.getShowCategory(shopId);
		return new BaseResponse(categories);
		
	}
	
}
