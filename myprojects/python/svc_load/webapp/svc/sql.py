#coding: utf-8

# __all__  = [
#     "query_client_sql",
#     "add_client_sql",
#     "delete_client_sql",
#     "query_enable_client"
# ]

query_client_sql = '''
    SELECT id,client_ip,role,slave_count,`status` FROM svc_load_client;
'''
add_client_sql = '''
    INSERT INTO svc_load_client {0[tkey]} VALUES {0[tvalue]} ON DUPLICATE KEY UPDATE {0[tstring]}
'''
delete_client_sql = '''
    delete from svc_load_client WHERE id=%s
'''
enable_client_count_sql = '''
    SELECT COUNT(1)*slave_count AS client_num FROM svc_load_client WHERE `status`=1
'''
enable_clients_ip_sql = '''
    SELECT client_ip,slave_count FROM svc_load_client WHERE `status`=1 AND role!=1;
'''
master_ip_sql = '''
    SELECT id, client_ip FROM svc_load_client WHERE `status`=1 AND role=1 limit 1;
'''
locust_master_ip_sql = '''
    SELECT value from common_config WHERE id=5
'''
get_test_record_sql = '''
    SELECT * FROM load_test_record WHERE `status`!=0;
'''
