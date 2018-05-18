package com.vdcoding.modules.test.entity;

import org.hibernate.validator.constraints.NotBlank;

import java.io.Serializable;

/**
 * 性能测试用例文件
 */
public class StressTestFileEntity implements Serializable {

    private static final long serialVersionUID = 1L;

    /**
     * 主键id
     */
    private Long fileId;

    /**
     * 用例名称
     */
    @NotBlank(message="所属用例不能为空")
    private String caseId;

    /**
     * 用例文件名
     */
    @NotBlank(message="文件名不能为空")
    private String originName;

    /**
     * 用例保存文件名，唯一化
     */
    private String fileName;

    /**
     * MD5唯一标识
     */
    private String digest;

    /**
     * 提交的用户
     */
    private String addBy;

    /**
     * 修改的用户
     */
    private String updateBy;


    /**
     * 提交的时间
     */
    private String addTime;

    public Long getFileId() {
        return fileId;
    }

    public void setFileId(Long fileId) {
        this.fileId = fileId;
    }

    public String getCaseId() {
        return caseId;
    }

    public void setCaseId(String caseId) {
        this.caseId = caseId;
    }

    public String getOriginName() {
        return originName;
    }

    public void setOriginName(String originName) {
        this.originName = originName;
    }

    public String getDigest() {
        return digest;
    }

    public void setDigest(String digest) {
        this.digest = digest;
    }

    public String getAddBy() {
        return addBy;
    }

    public void setAddBy(String addBy) {
        this.addBy = addBy;
    }

    public String getUpdateBy() {
        return updateBy;
    }

    public void setUpdateBy(String updateBy) {
        this.updateBy = updateBy;
    }

    public String getFileName() {
        return fileName;
    }

    public void setFileName(String fileName) {
        this.fileName = fileName;
    }

    public String getAddTime() {
        return addTime;
    }

    public void setAddTime(String addTime) {
        this.addTime = addTime;
    }
}
