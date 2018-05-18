package com.vdcoding.modules.superman.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.vdcoding.modules.superman.dao.PageDao;
import com.vdcoding.modules.superman.pojos.Page;
import com.vdcoding.modules.superman.service.PageService;


@Service
public class PageServiceImpl implements PageService{
	
	@Autowired
	PageDao pageDao;
	
	public Page getPage(int pageId){
		return pageDao.getPage(pageId);
	}
}
