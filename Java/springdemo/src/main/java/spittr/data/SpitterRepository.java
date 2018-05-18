package spittr.data;

import java.util.List;
import java.util.Map;

import spittr.Client;

public interface SpitterRepository {

  List<Map<String, Object>> findClientByID(String id);
  
  int saveClient(Client client);
  
  List<Map<String, Object>> findAllClient();
  
  int deleteClient(String id);
  
  int updateClient(Client client);

}
