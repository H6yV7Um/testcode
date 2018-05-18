package com.vdcoding.modules.test.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.vdcoding.modules.test.dao.StressTestDao;
import com.vdcoding.modules.test.entity.StressTestEntity;
import com.vdcoding.modules.test.service.StressTestService;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service("stressTestService")
public class StressTestServiceImpl implements StressTestService {

    @Autowired
    private StressTestDao stressTestDao;

    @Override
    public StressTestEntity queryObject(Long caseId) {
        return stressTestDao.queryObject(caseId);
    }

    @Override
    public List<StressTestEntity> queryList(Map<String, Object> map) {
        return stressTestDao.queryList(map);
    }

    @Override
    public int queryTotal(Map<String, Object> map) {
        return stressTestDao.queryTotal(map);
    }

    @Override
    public void save(StressTestEntity stressCase) {
        stressTestDao.save(stressCase);
    }

    @Override
    public void update(StressTestEntity stressCase) {
        stressTestDao.update(stressCase);

    }

    @Override
    public void deleteBatch(Long[] caseIds) {
        stressTestDao.deleteBatch(caseIds);
    }

    @Override
    public int updateBatch(Long[] caseIds, int status) {
        Map<String, Object> map = new HashMap<>();
        map.put("list", caseIds);
        map.put("status", status);
        return stressTestDao.updateBatch(map);
    }

    /**
     *
     * @param caseIds
     */
    @Override
    public void run(Long[] caseIds) {

    }

    @Override
    public void stop(Long[] caseIds) {

    }

    @Override
    public void stopNow(Long[] caseIds) {

    }
}
