from svccore.ProtoBody_pb2 import ClientAccessReq, GetAccessServerRsp


# client = ClientAccessReq()
# client.app_id = "123"
# client.cli_mac = "321"
# client.cli_type = 1
# client.cli_version = "3"
# client.cli_os_ver = 2
# client.device_id = b"555"

# bdata = client.SerializeToString()
# print(bdata)
# client.ParseFromString(bdata)
# d = {k.name:v for k,v in dict(client.ListFields()).items()}
# print(d)
rsp = GetAccessServerRsp()
bstr = b'\x12\x0c\x08\x99\xa0\xc0\xe0\n\x12\x04\xa4&\xbb\x03'
rsp.ParseFromString(bstr)
print(rsp.ListFields()[0][1])
d = {k.name:v for k,v in dict(rsp.ListFields()).items()}
print(d)




