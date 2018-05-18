package com.vdcoding.modules.superman.controller;

import java.util.HashMap;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.vdcoding.modules.superman.common.BaseResponse;
import com.vdcoding.modules.superman.pojos.Page;
import com.vdcoding.modules.superman.service.impl.PageServiceImpl;

@RestController
@RequestMapping(path="/customer/layout")
public class LayoutController {
	@Autowired
	PageServiceImpl pageService;
	
	@GetMapping(path="/page/{pageId}")
	public BaseResponse getPage(@PathVariable int pageId){
		Page page = pageService.getPage(pageId);
		HashMap<String, Object> result = new HashMap<>();
		result.put("message", page);
		return new BaseResponse(result);
		
	}
}
