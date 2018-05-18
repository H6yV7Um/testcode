package com.vdcoding.modules.superman.service;

import com.vdcoding.modules.superman.common.BaseResponse;
import com.vdcoding.modules.superman.pojos.CustomerToken;

public interface CustomerTokenService {

	CustomerToken queryByCustomerId(int customerId);
	
	CustomerToken queryByToken(String token);
	
	int getCustomerIdByToken(String token);

	void save(CustomerToken token);
	
	void update(CustomerToken token);

	/**
	 * 生成token
	 * @param userId  用户ID
	 */
	BaseResponse createOrUpdateToken(int customerId);

	/**
	 * 退出，修改token值
	 * @param userId  用户ID
	 */
	void logout(int customerId);

}
