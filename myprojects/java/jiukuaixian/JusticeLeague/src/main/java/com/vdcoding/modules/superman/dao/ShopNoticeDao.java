package com.vdcoding.modules.superman.dao;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.vdcoding.modules.superman.pojos.ShopNotice;
import com.vdcoding.modules.sys.dao.BaseDao;

@Mapper
public interface ShopNoticeDao extends BaseDao<ShopNotice>{
	List<ShopNotice> getByShopId(int shopId);
}
