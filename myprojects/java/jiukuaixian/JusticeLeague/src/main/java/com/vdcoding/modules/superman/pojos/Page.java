package com.vdcoding.modules.superman.pojos;

import java.io.Serializable;
import java.util.List;

public class Page implements Serializable{

	private static final long serialVersionUID = 1L;
	
	private int id;
	private String name;
	private String type;
	private List<PageComponent> components;
	private List<PagePlugin> plugins;
	
	public int getId() {
		return id;
	}
	public void setId(int id) {
		this.id = id;
	}
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public String getType() {
		return type;
	}
	public void setType(String type) {
		this.type = type;
	}
	public List<PageComponent> getComponents() {
		return components;
	}
	public void setComponents(List<PageComponent> components) {
		this.components = components;
	}
	public List<PagePlugin> getPlugins() {
		return plugins;
	}
	public void setPlugins(List<PagePlugin> plugins) {
		this.plugins = plugins;
	}
	

}
