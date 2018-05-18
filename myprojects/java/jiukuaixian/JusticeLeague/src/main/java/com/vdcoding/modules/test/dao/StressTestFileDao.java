package com.vdcoding.modules.test.dao;

import org.apache.ibatis.annotations.Mapper;

import com.vdcoding.modules.sys.dao.BaseDao;
import com.vdcoding.modules.test.entity.StressTestFileEntity;

@Mapper
public interface StressTestFileDao extends BaseDao<StressTestFileEntity> {


}
