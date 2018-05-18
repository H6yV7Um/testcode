package com.vdcoding.modules.app.utils;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

/**
 * 性能测试的工具类，用于读取配置文件。
 */
@ConfigurationProperties(prefix = "test.stress")
@Component
public class StressTestUtils {

    private String jmeterPath;

    public String getJmeterPath() {
        return jmeterPath;
    }

    public void setJmeterPath(String jmeterPath) {
        this.jmeterPath = jmeterPath;
    }
}
