package com.vdcoding.modules.test.controller;

import org.apache.shiro.authz.annotation.RequiresPermissions;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import com.vdcoding.common.annotation.SysLog;
import com.vdcoding.common.utils.PageUtils;
import com.vdcoding.common.utils.Query;
import com.vdcoding.common.utils.R;
import com.vdcoding.modules.test.entity.StressTestFileEntity;
import com.vdcoding.modules.test.service.StressTestFileService;

import java.util.List;
import java.util.Map;

/**
 * 压力测试用例文件
 *
 */
@RestController
@RequestMapping("/test/stressFile")
public class StressTestFileController {
    @Autowired
    private StressTestFileService stressTestFileService;

    /**
     * 定时任务日志列表
     */
    @RequestMapping("/list")
    @RequiresPermissions("test:stress:fileList")
    public R list(@RequestParam Map<String, Object> params){
        //查询列表数据
        Query query = new Query(params);
        List<StressTestFileEntity> jobList = stressTestFileService.queryList(query);
        int total = stressTestFileService.queryTotal(query);

        PageUtils pageUtil = new PageUtils(jobList, total, query.getLimit(), query.getPage());

        return R.ok().put("page", pageUtil);
    }

    /**
     * 查询具体文件信息
     */
    @RequestMapping("/info/{fileId}")
    public R info(@PathVariable("fileId") Long fileId){
        StressTestFileEntity file = stressTestFileService.queryObject(fileId);
        return R.ok().put("file", file);
    }

    /**
     * 删除性能测试用例
     */
    @SysLog("删除性能测试用例")
    @RequestMapping("/delete")
    @RequiresPermissions("test:stress:fileDelete")
    public R delete(@RequestBody Long[] fileIds) {
        stressTestFileService.deleteBatch(fileIds);

        return R.ok();
    }

}