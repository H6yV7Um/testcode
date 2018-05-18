package com.vdcoding.modules.superman.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.vdcoding.modules.superman.common.BaseResponse;
import com.vdcoding.modules.superman.pojos.CustomerAddress;
import com.vdcoding.modules.superman.service.CustomerService;
import com.vdcoding.modules.superman.service.CustomerTokenService;

@RestController
@RequestMapping(path="/customer/addresses")
public class AddressController {
	
	@Autowired
	CustomerService customerService;
	
	@Autowired
	CustomerTokenService customerTokenService;
	
	/*
	 * 目前没有对配送地址做限制，会返回所有地址列表
	 */
	@GetMapping(path={"/available", ""})
	public BaseResponse getAvailableAddress(@RequestHeader(name="token")String token){
		int customerId = customerTokenService.getCustomerIdByToken(token);
		List<CustomerAddress> addresses = customerService.getAvailableAddress(customerId);
		return BaseResponse.ok(addresses);
	}
	
	/*
	 * 新增收货地址
	 */
	@PostMapping(path="")
	public BaseResponse addAddress(@RequestBody CustomerAddress address, @RequestHeader(name="token")String token){
		int customerId = customerTokenService.getCustomerIdByToken(token);
		address.setCustomerId(customerId);
		customerService.addAddress(address);
		return BaseResponse.ok();
	}
	
	/*
	 * 设置默认收货地址
	 */
	@GetMapping(path="/{addressId}/default")
	public BaseResponse setDefaultAddress(@PathVariable int addressId){
		customerService.setDefaultAddress(addressId);
		return BaseResponse.ok();
	}
	/*
	 * 获取地址信息
	 */
	@GetMapping(path="/{addressId}")
	public BaseResponse getAddress(@PathVariable int addressId){
		CustomerAddress address = customerService.getAddress(addressId);
		return BaseResponse.ok(address);
	}
	
	/*
	 * 更新地址信息
	 */
	@PostMapping(path="{addressId}")
	public BaseResponse updateAddress(@RequestBody CustomerAddress address){
		customerService.updateAddress(address);
		return BaseResponse.ok();
	}

}
