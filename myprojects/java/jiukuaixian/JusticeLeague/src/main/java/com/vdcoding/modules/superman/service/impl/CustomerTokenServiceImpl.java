package com.vdcoding.modules.superman.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.vdcoding.modules.superman.common.BaseResponse;
import com.vdcoding.modules.superman.common.exception.CustomerNotExistsError;
import com.vdcoding.modules.superman.dao.CustomerTokenDao;
import com.vdcoding.modules.superman.pojos.CustomerToken;
import com.vdcoding.modules.superman.service.CustomerTokenService;
import com.vdcoding.modules.sys.oauth2.TokenGenerator;

import java.util.Date;


@Service
public class CustomerTokenServiceImpl implements CustomerTokenService {
	@Autowired
	private CustomerTokenDao customerTokenDao;
	//9999小时后过期
	private final static int EXPIRE = 9999 * 3600 * 1000;

	@Override
	public CustomerToken queryByCustomerId(int customerId) {
		return customerTokenDao.queryByCustomerId(customerId);
	}
	
	@Override
	public CustomerToken queryByToken(String token){
		return customerTokenDao.queryByToken(token);	
	}
	
	@Override
	public int getCustomerIdByToken(String token) {
		CustomerToken customerToken = queryByToken(token);
		return customerToken.getCustomerId();
	}

	@Override
	public void save(CustomerToken token){
		customerTokenDao.save(token);
	}
	
	@Override
	public void update(CustomerToken token){
		customerTokenDao.update(token);
	}

	@Override
	public BaseResponse createOrUpdateToken(int customerId) {
		//生成一个token
		String token = TokenGenerator.generateValue();

		//当前时间
		Date now = new Date();
		//过期时间
		Date expireTime = new Date(now.getTime() + EXPIRE);

		//判断是否生成过token
		CustomerToken customerToken = queryByCustomerId(customerId);
		if(customerToken == null){
			customerToken = new CustomerToken();
			customerToken.setCustomerId(customerId);
			customerToken.setToken(token);
			customerToken.setUpdateTime(now);
			customerToken.setExpireTime(expireTime);

			//保存token
			save(customerToken);
		}else{
			customerToken.setToken(token);
			customerToken.setUpdateTime(now);
			customerToken.setExpireTime(expireTime);

			//更新token
			update(customerToken);
		}

		return new BaseResponse(token);
	}

	@Override
	public void logout(int customerId) {
		//生成一个token
		String token = TokenGenerator.generateValue();

		//修改token
		CustomerToken customerToken = new CustomerToken();
		customerToken.setCustomerId(customerId);
		customerToken.setToken(token);
		update(customerToken);
	}
	
}
