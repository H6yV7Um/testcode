package com.vdcoding.modules.superman.dao;

import org.apache.ibatis.annotations.Mapper;

import com.vdcoding.modules.superman.pojos.Customer;
import com.vdcoding.modules.sys.dao.BaseDao;

@Mapper
public interface CustomerDao extends BaseDao<Customer>{
	Customer getCustomerById(int id);
	Customer getCustomerByOpenId(String openId);
}
