package com.vdcoding.mybatis.pojos;


public class User {
	//属性名和数据库表的字段对应  
    private int id;  
    private String username;
    private String sex;
    private int phone;
    private String address;
    public int getId() {  
        return id;  
    }  

    public String getUsername() {  
        return username;  
    }  
    public void setUsername(String username) {  
        this.username = username;  
    }  
    public String getSex() {  
        return sex;  
    }  
    public void setSex(String sex) {  
        this.sex = sex;  
    }  
    public int getPhone() {  
        return phone;  
    }  
    public void setPhone(int phone) {  
        this.phone = phone;  
    }  
    public String getAddress() {  
        return address;  
    }  
    public void setAddress(String address) {  
        this.address = address;  
    }  
    @Override  
    public String toString() {  
        return "User [id=" + id + ", username=" + username + ", sex=" + sex + "]";  
    }  
}
