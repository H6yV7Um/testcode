package com.vdcoding.modules.superman.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.vdcoding.modules.superman.common.BaseResponse;
import com.vdcoding.modules.superman.service.ShopService;

@RestController
@RequestMapping("/customer/shops")
public class ShopController {
	
	@Autowired
	ShopService shopService;
	
	@GetMapping(path="/full")
	public BaseResponse getFullShopInfo(@RequestParam(name="shop_id",defaultValue="3")int shopId){
		return new BaseResponse(shopService.getFullShopInfo(shopId));
	}
	
	@GetMapping(path="/status")
	public BaseResponse checkShopStatus(@RequestParam(name="shop_id",defaultValue="3")int shopId){
		return BaseResponse.ok(shopService.isShopOpen(shopId));
	}
}
