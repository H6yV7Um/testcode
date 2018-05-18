package com.vdcoding.modules.superman.dao;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.vdcoding.modules.superman.pojos.GoodsCategory;
import com.vdcoding.modules.sys.dao.BaseDao;

@Mapper
public interface GoodsCategoryDao extends BaseDao<GoodsCategory>{
	
	List<GoodsCategory> getShowCategory(int shopId);

}
