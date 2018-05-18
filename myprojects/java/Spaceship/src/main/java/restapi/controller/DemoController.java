package restapi.controller;

import static org.springframework.web.bind.annotation.RequestMethod.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.validation.Valid;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.validation.Errors;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

import restapi.pojo.Client;
import restapi.data.DemoClientRepository;;

//@RestController
@RequestMapping("/test")
public class DemoController {
  
	private final Logger logger=LoggerFactory.getLogger(this.getClass());
	private DemoClientRepository spitterRepository;
  
	  @Autowired
	  public DemoController(DemoClientRepository spitterRepository) {
	    this.spitterRepository = spitterRepository;
	  }
	  
	  @RequestMapping(value="/getclient", method=GET)
	  public List<?> getClient(@RequestParam(value="id", defaultValue="all") String id){
		  if (id.equalsIgnoreCase("all")){
			  return spitterRepository.findAllClient();
		  }
		  return spitterRepository.findClientByID(id);
		  
	  }
	  
	  @RequestMapping(value="/deleteclient", method=GET)
	  public Map<String, ?> deleteClient(@RequestParam(value="id") String id){
		  Map<String, String> msg = new HashMap<String, String>();
		  try {
			int affectedRow = spitterRepository.deleteClient(id);
			if (affectedRow>0){
				msg.put("status", "succcess");
			}
			else {
				msg.put("status", "fail");
			}
			msg.put("num", String.valueOf(affectedRow));
			return msg;
		} catch (Exception e) {
			// TODO: handle exception
			msg.put("status", "error");
			msg.put("error", e.getMessage());
			return msg;
		}
		  finally {
			  logger.info("delete client:"+ id);
		}
	  }
	  
	  @RequestMapping(value="/createclient", method=POST, consumes="application/json")
	  public Map<String, ?> createClient(@RequestBody@Valid Client client, Errors error){
		  Map<String, String> msg = new HashMap<String, String>();
		  if (error.hasErrors()){
			  msg.put("status", "fail");
			  msg.put("error", error.toString());
			  return msg;
		  }
		  spitterRepository.saveClient(client);
		  msg.put("status", "success");
		  //java 中任何对象都可转化为字符串，通过+或者toString
		  msg.put("client", client.toString());
		  return msg;
	  }
	  
	  @RequestMapping(value="/updateclient", method=POST)
	  public ResponseEntity<Client> updateClient(@RequestBody Client client){
//		  int affectedRow = spitterRepository.updateClient(client);
		  HttpHeaders headers = new HttpHeaders();
		  headers.setAccessControlAllowOrigin("*");
		  ResponseEntity<Client> responseEntity = new ResponseEntity<Client>(client, headers, HttpStatus.OK);
		  return responseEntity;
	  }
	  
  
}
