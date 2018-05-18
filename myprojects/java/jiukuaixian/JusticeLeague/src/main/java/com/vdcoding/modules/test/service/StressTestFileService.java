package com.vdcoding.modules.test.service;

import java.util.List;
import java.util.Map;

import com.vdcoding.modules.test.entity.StressTestFileEntity;

/**
 * 性能测试压测文件
 */
public interface StressTestFileService {

    /**
     * 根据ID，查询文件
     */
    StressTestFileEntity queryObject(Long fileId);

    /**
     * 查询文件列表
     */
    List<StressTestFileEntity> queryList(Map<String, Object> map);

    /**
     * 查询总数
     */
    int queryTotal(Map<String, Object> map);

    /**
     * 保存性能测试用例文件
     */
    void save(StressTestFileEntity stressCaseFile);

    /**
     * 更新性能测试用例信息
     */
    void update(StressTestFileEntity stressCaseFile);

    /**
     * 批量删除
     */
    void deleteBatch(Long[] fileIds);

//    /**
//     * 批量更新性能测试用例信息
//     */
//    int updateBatch(Long[] caseIds, int status);

//    /**
//     * 立即执行
//     */
//    void run(Long[] caseIds);
//
//    /**
//     * 停止运行
//     */
//    void stop(Long[] caseIds);
//
//    /**
//     * 立即停止运行
//     */
//    void stopNow(Long[] caseIds);

}
