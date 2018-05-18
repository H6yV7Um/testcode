package com.vdcoding.modules.superman.pojos;

import java.io.Serializable;

public class ComponentData implements Serializable {

	private static final long serialVersionUID = 1L;
	
	private int id;
	private int componentId;
	private int seq;
	private String title;
	private String action;
	private String url;
	private String iconClass;
	private String iconColor;
	private String iconSize;
	private ComponentTarget targetId;
	
	public int getId() {
		return id;
	}
	public void setId(int id) {
		this.id = id;
	}
	public int getComponentId() {
		return componentId;
	}
	public void setComponentId(int componentId) {
		this.componentId = componentId;
	}
	
	public ComponentTarget getTargetId() {
		return targetId;
	}
	public void setTargetId(ComponentTarget targetId) {
		this.targetId = targetId;
	}
	public int getSeq() {
		return seq;
	}
	public void setSeq(int seq) {
		this.seq = seq;
	}
	public String getTitle() {
		return title;
	}
	public void setTitle(String title) {
		this.title = title;
	}
	public String getAction() {
		return action;
	}
	public void setAction(String action) {
		this.action = action;
	}
	public String getUrl() {
		return url;
	}
	public void setUrl(String url) {
		this.url = url;
	}
	public String getIconClass() {
		return iconClass;
	}
	public void setIconClass(String iconClass) {
		this.iconClass = iconClass;
	}
	public String getIconColor() {
		return iconColor;
	}
	public void setIconColor(String iconColor) {
		this.iconColor = iconColor;
	}
	public String getIconSize() {
		return iconSize;
	}
	public void setIconSize(String iconSize) {
		this.iconSize = iconSize;
	}
	
}
