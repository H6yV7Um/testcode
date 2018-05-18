package com.vdcoding.modules.superman.dao;

import org.apache.ibatis.annotations.Mapper;

import com.vdcoding.modules.superman.pojos.PageComponent;
import com.vdcoding.modules.superman.pojos.Page;
import com.vdcoding.modules.sys.dao.BaseDao;


@Mapper
public interface PageDao extends BaseDao<PageComponent>{
	Page getPage(int pageId);
}
