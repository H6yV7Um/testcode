package spittr.data;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.List;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.jdbc.core.JdbcOperations;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Repository;
//import org.springframework.test.context.ActiveProfiles;

import spittr.Client;


@Repository
public class JdbcSpitterRepository implements SpitterRepository {
  
  private JdbcOperations jdbc;
  private final Logger logger = LoggerFactory.getLogger(this.getClass());

  @Autowired
  public JdbcSpitterRepository(JdbcOperations jdbc) {
    this.jdbc = jdbc;
  }

  public int saveClient(Client client){
	  int affectedRow = jdbc.update(
		"insert into svc_load_client (client_ip, role, status, slave_count) values (?,?,?,?)",
		client.getIP(),
		client.getRole(),
		client.getStatus(),
		client.getSlaveCount());
	  return affectedRow;
  }
  
  public int updateClient(Client client){
	  int affectedRow = jdbc.update(
		"update svc_load_client set client_ip=?, role=?, status=?, slave_count=? where id=?",
		client.getIP(),
		client.getRole(),
		client.getStatus(),
		client.getSlaveCount(),
		client.getID());
	  return affectedRow;
  }
  
  public int deleteClient(String id){
	  int affectedRow = jdbc.update(
		"delete from svc_load_client where id=?",
		id);
	  return affectedRow;
  }
  
  public List<Map<String, Object>> findClientByID(String id){
	  return jdbc.queryForList(
		"select id, client_ip, role, status, slave_count from svc_load_client where id=?;",
		id);
  }

  public List<Map<String, Object>> findAllClient(){
	  return jdbc.queryForList(
		"select id, client_ip, role, status, slave_count from svc_load_client");
  }
  
  private static final class ClientRowMapper implements RowMapper<Client> {
	    public Client mapRow(ResultSet rs, int rowNum) throws SQLException {
	    	System.out.println(rowNum);
	    	if (rowNum!=0){
	    		return new Client(
		          rs.getString("id"),
		          rs.getString("client_ip"),
		          rs.getString("role"),
		          rs.getString("status"),
		          rs.getString("slave_count"));
	    	}
	    	else {
	    		return new Client("122", "172.16.16.74", "2", "3", "hellotest");
	    	}
	      
	    }
	  }
 

}
