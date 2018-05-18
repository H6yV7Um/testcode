package com.vdcoding.modules.test.controller;

import org.apache.shiro.authz.annotation.RequiresPermissions;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import com.vdcoding.common.annotation.SysLog;
import com.vdcoding.common.exception.RRException;
import com.vdcoding.common.utils.PageUtils;
import com.vdcoding.common.utils.Query;
import com.vdcoding.common.utils.R;
import com.vdcoding.common.validator.ValidatorUtils;
import com.vdcoding.modules.test.entity.StressTestEntity;
import com.vdcoding.modules.test.entity.StressTestFileEntity;
import com.vdcoding.modules.test.service.StressTestFileService;
import com.vdcoding.modules.test.service.StressTestService;

import javax.servlet.http.HttpServletRequest;
import java.util.List;
import java.util.Map;

/**
 * 性能测试
 */
@RestController
@RequestMapping("/test/stress")
public class StressTestController {
    @Autowired
    private StressTestService stressTestService;

    @Autowired
    private StressTestFileService stressTestFileService;

    /**
     * 性能测试用例列表
     */
    @RequestMapping("/list")
    @RequiresPermissions("test:stress:list")
    public R list(@RequestParam Map<String, Object> params) {
        //查询列表数据
        Query query = new Query(params);
        List<StressTestEntity> stressTestList = stressTestService.queryList(query);
        int total = stressTestService.queryTotal(query);

        PageUtils pageUtil = new PageUtils(stressTestList, total, query.getLimit(), query.getPage());

        return R.ok().put("page", pageUtil);
    }

    /**
     * 性能测试用例信息
     */
    @RequestMapping("/info/{caseId}")
    @RequiresPermissions("test:stress:info")
    public R info(@PathVariable("caseId") Long stressTestId) {
        StressTestEntity stressCase = stressTestService.queryObject(stressTestId);

        return R.ok().put("stressCase", stressCase);
    }


    /**
     * 上传文件
     */
    @RequestMapping("/upload")
    @RequiresPermissions("test:stress:upload")
    public R upload(@RequestParam("file") MultipartFile file, HttpServletRequest request) throws Exception {

        if (file.isEmpty()) {
            throw new RRException("上传文件不能为空");
        }

        String caseId = request.getParameter("caseIds");

        //上传文件
        String suffix = file.getOriginalFilename().substring(file.getOriginalFilename().lastIndexOf("."));
//        String url = OSSFactory.build().uploadSuffix(file.getBytes(), suffix);

        //保存文件信息
        StressTestFileEntity stressCaseFile = new StressTestFileEntity();
        stressCaseFile.setCaseId(caseId);
        stressCaseFile.setOriginName(file.getOriginalFilename());
        stressTestFileService.save(stressCaseFile);

        return R.ok().put("url", suffix);
    }


    /**
     * 保存性能测试用例
     */
    @SysLog("保存性能测试用例")
    @RequestMapping("/save")
    @RequiresPermissions("test:stress:save")
    public R save(@RequestBody StressTestEntity stressTestCase) {
        ValidatorUtils.validateEntity(stressTestCase);
        //status并非前台修改新增传入的，所以要替换掉默认值
        if (stressTestCase.getStatus() == null) {
            stressTestCase.setStatus(0);
        }

        stressTestService.save(stressTestCase);

        return R.ok();
    }

    /**
     * 修改性能测试用例
     */
    @SysLog("修改性能测试用例")
    @RequestMapping("/update")
    @RequiresPermissions("test:stress:update")
    public R update(@RequestBody StressTestEntity stressTestCase) {
        ValidatorUtils.validateEntity(stressTestCase);

        //status并非前台修改新增传入的，所以要替换掉默认值
        if (stressTestCase.getStatus() == null) {
            stressTestCase.setStatus(0);
        }

        stressTestService.update(stressTestCase);

        return R.ok();
    }

    /**
     * 删除性能测试用例
     */
    @SysLog("删除性能测试用例")
    @RequestMapping("/delete")
    @RequiresPermissions("test:stress:delete")
    public R delete(@RequestBody Long[] caseIds) {
        stressTestService.deleteBatch(caseIds);

        return R.ok();
    }

    /**
     * 立即性能测试用例，当前仅支持同一时间执行一个性能测试用例。
     */
    @SysLog("立即性能测试用例")
    @RequestMapping("/runOnce")
    @RequiresPermissions("test:stress:runOnce")
    public R run(@RequestBody Long[] caseIds) {
        stressTestService.run(caseIds);

        return R.ok();
    }

    /**
     * 停止性能测试用例
     */
    @SysLog("停止性能测试用例")
    @RequestMapping("/stop")
    @RequiresPermissions("test:stress:stop")
    public R stop(@RequestBody Long[] caseIds) {
        stressTestService.stop(caseIds);

        return R.ok();
    }

    /**
     * 立即停止性能测试用例，后台是杀掉进程
     */
    @SysLog("立即停止性能测试用例")
    @RequestMapping("/stopNow")
    @RequiresPermissions("test:stress:stopNow")
    public R stopNow(@RequestBody Long[] caseIds) {
        stressTestService.stopNow(caseIds);

        return R.ok();
    }


}
