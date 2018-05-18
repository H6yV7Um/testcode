package com.vdcoding.modules.test.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.vdcoding.modules.test.dao.StressTestFileDao;
import com.vdcoding.modules.test.entity.StressTestFileEntity;
import com.vdcoding.modules.test.service.StressTestFileService;

import java.util.List;
import java.util.Map;

@Service("stressTestFileService")
public class StressTestFileServiceImpl implements StressTestFileService {

    @Autowired
    private StressTestFileDao stressTestFileDao;

    @Override
    public StressTestFileEntity queryObject(Long fileId) {
        return stressTestFileDao.queryObject(fileId);
    }

    @Override
    public List<StressTestFileEntity> queryList(Map<String, Object> map) {
        return stressTestFileDao.queryList(map);
    }

    @Override
    public int queryTotal(Map<String, Object> map) {
        return stressTestFileDao.queryTotal(map);
    }

    @Override
    public void save(StressTestFileEntity stressCaseFile) {
        stressTestFileDao.save(stressCaseFile);
    }

    @Override
    public void update(StressTestFileEntity stressCaseFile) {
        stressTestFileDao.update(stressCaseFile);
    }

    @Override
    public void deleteBatch(Long[] fileIds) {
        stressTestFileDao.deleteBatch(fileIds);
    }
}
