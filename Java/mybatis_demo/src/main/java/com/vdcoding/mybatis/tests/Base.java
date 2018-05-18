package com.vdcoding.mybatis.tests;

import java.io.IOException;

import java.io.InputStream;

import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;

/*
 * 1、由于mybatis是基于OGNL表达式来查找属性，所以定义mapper xml时，会根据占位符中的名称去对应的parameterType中获取，
 * 比如parameterType=User，则#{sex}会调用user对象的getSex方法去获取值，
 * 但是对于基本类型 比如parameterType=String，如果占位符是#{name}，此时就会报错There is no getter for property named 'name' in 'class java.lang.String'
 * 因为string没有name属性,但是改为value或_parameter即可，参考https://www.cnblogs.com/lzzj/p/3991128.html
 */

public class Base {
	// mybatis配置文件  
	private String resource = "mybatis-config.xml";
	private InputStream is;
	private SqlSessionFactory sessionFactory;
	public SqlSession session;
	
	public Base() throws IOException {
		// 得到配置文件流  
		is = Resources.getResourceAsStream(resource);
		// 通过配置流构建会话工厂
		sessionFactory = new SqlSessionFactoryBuilder().build(is);
		// 通过工厂得到SqlSession ,传入true启用autoCommit，如果无参调用openSession则默认开启一个事物，即需要手动commit
		session = sessionFactory.openSession(true);
	}
	public Base(String env) throws IOException{
		is = Resources.getResourceAsStream(resource);
		//构建sessionFactory时如果传入env参数，则会引用在mybatis-config.xml中id为对应值的environment配置
		//比如传入production，则会引用<environment id="production">中定义的配置来构建数据源，这样便于多数据库访问
		//如果只传入配置文件流is，则会使用mybatis-config.xml中定义的默认配置<environments default="development">  
		sessionFactory = new SqlSessionFactoryBuilder().build(is, env);
		session = sessionFactory.openSession(true);
	}
}
