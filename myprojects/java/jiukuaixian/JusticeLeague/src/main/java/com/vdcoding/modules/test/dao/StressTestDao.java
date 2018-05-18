package com.vdcoding.modules.test.dao;

import org.apache.ibatis.annotations.Mapper;

import com.vdcoding.modules.sys.dao.BaseDao;
import com.vdcoding.modules.test.entity.StressTestEntity;

import java.util.Map;

/**
 * 性能测试
 * 
 */
@Mapper
public interface StressTestDao extends BaseDao<StressTestEntity> {
	
	/**
	 * 批量更新状态
	 */
	int updateBatch(Map<String, Object> map);
}
