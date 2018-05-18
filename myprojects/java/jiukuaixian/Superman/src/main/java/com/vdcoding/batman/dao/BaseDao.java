package com.vdcoding.batman.dao;

import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;
import org.springframework.beans.factory.annotation.Autowired;


public class BaseDao {
	
	SqlSessionFactory sqlSessionFactory;
	SqlSession sqlSession;
	
	@Autowired
	public BaseDao(SqlSessionFactory factory) {
		this.sqlSessionFactory = factory;
		this.sqlSession = this.sqlSessionFactory.openSession();
	}
}
