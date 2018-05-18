package com.vdcoding.modules.superman.utils;

import java.time.LocalTime;

public class DateUtil {
	public static boolean isAfterNow(String beginTime){
		LocalTime now = LocalTime.now();
		return false;
	}
	
	public static void main(String...args){
		LocalTime now = LocalTime.now();
		String begin = "23:59:59";
		LocalTime beginTime = LocalTime.parse(begin);
		System.out.println(now.isAfter(beginTime));
	}
}
