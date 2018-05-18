package com.vdcoding;


public class Perm {
	private int count = 0;
	
	public void permTest(int[] list,int b){
		int begin=b;
		int end = list.length;
		if(begin >= end){
//			System.out.println(Arrays.toString(list));;
			this.count++;
		}else{
			for(int i=begin;i<end;i++){
				int temp = list[i];
				list[i] = list[begin];
				list[begin] = temp;
				permTest(list, begin+1);
				int temp2 = list[i];
				list[i] = list[begin];
				list[begin] = temp2;
			}
		}
	}
	
	public static void main(String[] args){
		
		int len = 11;
		int[] list = new int[len];
		for(int i=0;i<len;i++){
			list[i] = i;
		}
		Perm perm = new Perm();
		long start = System.currentTimeMillis();
		perm.permTest(list, 0);
		//average elapsed time: 130 milliseconds
		long elapsed = System.currentTimeMillis() - start;
		System.out.println(perm.count);
		System.out.print(elapsed);
	}
}
