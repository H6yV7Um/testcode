package com.vdcoding.modules.superman.dao;

import org.apache.ibatis.annotations.Mapper;

import com.vdcoding.modules.superman.pojos.CustomerToken;
import com.vdcoding.modules.sys.dao.BaseDao;


@Mapper
public interface CustomerTokenDao extends BaseDao<CustomerToken> {
    
    CustomerToken queryByCustomerId(int userId);

    CustomerToken queryByToken(String token);
	
}
