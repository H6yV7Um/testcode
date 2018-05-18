package com.vdcoding.batman.service;

import javax.mail.MessagingException;

public interface MailService {

	public void sendSimpleEmail(String text);
	public void sendEmailWithAttachment() throws MessagingException;
}
