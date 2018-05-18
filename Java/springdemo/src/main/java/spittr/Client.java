package spittr;

import javax.validation.constraints.NotNull;

public class Client {

	private String id;
	@NotNull
	private String ip;
	@NotNull
	private String role;
	@NotNull
	private String status;
	@NotNull
	private String slaveCount;
	
	public Client(){};
	public Client(String ip, String role, String status, String slaveCount){
		this(null, ip, role, status, slaveCount);
	}
	
	public Client(String id, String ip, String role, String status, String slaveCount){
		this.id = id;
		this.ip = ip;
		this.role = role;
		this.status = status;
		this.slaveCount = slaveCount;
	}
	
	public String getID(){
		return id;
	}
	public void setID(String id){
		this.id = id;
	}
	
	public String getIP(){
		return ip;
	}
	public void setIP(String ip){
		this.ip = ip;
	}
	
	public String getRole(){
		return role;
	}
	public void setRole(String role){
		this.role = role;
	}
	
	public String getStatus(){
		return status;
	}
	public void setStatus(String status){
		this.status = status;
	}
	
	public String getSlaveCount(){
		return slaveCount;
	}
	public void setSlaveCount(String slaveCount){
		this.slaveCount = slaveCount;
	}
	
	public String toString(){
		return "client";
	}
	

	
}


