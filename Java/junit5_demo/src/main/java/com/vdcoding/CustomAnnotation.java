package com.vdcoding;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

import org.junit.jupiter.api.Tag;

/*
 * 自定义注解，在case用例文件中可以用@Standard或者@Repeat替换@Tag("standard")或者@Tag("repeat")
 * 由于修饰符权限问题，需要把该文件与用例文件放到同一个包下
 */
public class CustomAnnotation {

}


@Target({ ElementType.TYPE, ElementType.METHOD })
@Retention(RetentionPolicy.RUNTIME)
@Tag("standard")
@interface Standard {
}

@Target({ ElementType.TYPE, ElementType.METHOD })
@Retention(RetentionPolicy.RUNTIME)
@Tag("repeat")
@interface Repeat {
}