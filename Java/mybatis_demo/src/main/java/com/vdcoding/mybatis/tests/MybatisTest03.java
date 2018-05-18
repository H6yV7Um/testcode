package com.vdcoding.mybatis.tests;

import com.vdcoding.mybatis.mapper.ProductMapper;
import com.vdcoding.mybatis.pojos.Product;
import java.util.List;
import org.apache.ibatis.session.SqlSession;

public class MybatisTest03{

	public static void main(String[] args) throws Exception{
		SqlSession session = new Base().session;
		ProductMapper mapper = session.getMapper(ProductMapper.class);
		List<Product> products = mapper.getAllProduct();
		System.out.println(products);
	}
}
