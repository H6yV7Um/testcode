package com.vdcoding.datasources.aspect;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.aspectj.lang.reflect.MethodSignature;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.core.Ordered;
import org.springframework.stereotype.Component;

import com.vdcoding.datasources.DataSourceNames;
import com.vdcoding.datasources.DynamicDataSource;
import com.vdcoding.datasources.annotation.DataSource;

import java.lang.reflect.Method;

/**
 * 多数据源，切面处理类
 * @author chenshun
 * @email sunlightcs@gmail.com
 * @date 2017/9/16 22:20
 */
@Aspect
@Component
public class DataSourceAspect implements Ordered {
    protected Logger logger = LoggerFactory.getLogger(getClass());
    
    //@within针对类，@annotation针对方法
    @Pointcut("@within(com.vdcoding.datasources.annotation.DataSource)||@annotation(com.vdcoding.datasources.annotation.DataSource)")
    public void dataSourcePointCut() {

    }

    @Around("dataSourcePointCut()")
    public Object around(ProceedingJoinPoint point) throws Throwable {
        MethodSignature signature = (MethodSignature) point.getSignature();
        Method method = signature.getMethod();
        //首先获取方法上的注解
        DataSource ds = method.getAnnotation(DataSource.class);
        if(ds == null){
        	//获取类上的注解
        	ds = point.getTarget().getClass().getAnnotation(DataSource.class);
        	if(ds == null){
        		DynamicDataSource.setDataSource(DataSourceNames.FIRST);
                logger.debug("set datasource is " + DataSourceNames.FIRST);
                return false;
        	}
        }
        
        String dsKey = ds.name();
        if(dsKey != null){
        	DynamicDataSource.setDataSource(ds.name());
            logger.debug("set datasource is " + ds.name());
        }
            
        try {
            return point.proceed();
        } finally {
            DynamicDataSource.clearDataSource();
            logger.debug("clean datasource");
        }
    }

    @Override
    public int getOrder() {
        return 1;
    }
}
