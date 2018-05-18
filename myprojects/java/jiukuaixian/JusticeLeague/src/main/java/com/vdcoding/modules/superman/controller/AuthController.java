package com.vdcoding.modules.superman.controller;

import java.util.HashMap;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.vdcoding.modules.superman.common.BaseResponse;
import com.vdcoding.modules.superman.pojos.Customer;
import com.vdcoding.modules.superman.service.CustomerService;
import com.vdcoding.modules.superman.service.CustomerTokenService;
import com.vdcoding.modules.superman.utils.WepyUtil;

@RestController
@RequestMapping("/customer/auth")
public class AuthController {
	
	@Autowired
	CustomerService customerService;
	
	@Autowired
	CustomerTokenService customTokenService;
	
	@RequestMapping("/token")
	public BaseResponse getToken(@RequestParam(name="login_code")String loginCode) throws Exception{
		HashMap<String, Object> map = WepyUtil.getSessionKey(loginCode);
//		HashMap<String, Object> map = new HashMap<>();
//		map.put("open_id", "testhello");
		if(map.containsKey("errcode")){
			int errcode = (int)map.get("errcode");
			String errmsg = (String)map.get("errmsg");
			return new BaseResponse(errcode, errmsg);
		}
		String openId = (String)map.get("openid");
		//sessionKey暂时未使用，目前不需要用它来进行用户消息的加解密验证
//		String sessionKey = (String)map.get("session_key");
		Customer customer = customerService.getCustomerByOpenId(openId);
		if(customer != null){
			return customTokenService.createOrUpdateToken(customer.getId());
		}
		else{
			customer = new Customer();
			customer.setOpenId(openId);
			customer = customerService.saveAndGet(customer);
			return customTokenService.createOrUpdateToken(customer.getId());
		}
	}
	
	/*
	 * 目前觉得没有必要实现该接口，此处只为了方便前台调试
	 */
	@GetMapping(path="/check_session")
	public BaseResponse checkSession(){
		HashMap<String, String> result = new HashMap<>();
		result.put("result", "SUCCESS");
		return BaseResponse.ok(result);
	}
	
	/*
	 * 更新用户信息
	 */
	@PostMapping(path="/update_info")
	public BaseResponse updateCustomerInfo(@RequestHeader(name="token")String token, @RequestBody Customer customer){
		int customerId = customTokenService.getCustomerIdByToken(token);
		customer.setId(customerId);
		customerService.updateCustomer(customer);
		return BaseResponse.ok();
	}
}
