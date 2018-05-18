package com.vdcoding.datasources.annotation;

import java.lang.annotation.*;

/**
 * 多数据源注解
 * @author chenshun
 * @email sunlightcs@gmail.com
 * @date 2017/9/16 22:16
 */
@Target({ElementType.METHOD, ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface DataSource {
    String name() default "";
}
