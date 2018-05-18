package com.vdcoding.modules.superman.dao;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.vdcoding.modules.superman.pojos.CustomerAddress;
import com.vdcoding.modules.sys.dao.BaseDao;

@Mapper
public interface CustomerAddressDao extends BaseDao<CustomerAddress>{
	
	List<CustomerAddress> getAvailableAddress(int customerId);
	CustomerAddress getAddress(int id);
	CustomerAddress getDefaultAddress();
}
