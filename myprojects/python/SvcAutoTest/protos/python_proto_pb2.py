# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protos/python_proto.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='protos/python_proto.proto',
  package='test',
  syntax='proto3',
  serialized_pb=_b('\n\x19protos/python_proto.proto\x12\x04test\"\xa9\x02\n\nOnlineUser\x12\x10\n\x08rsp_code\x18\x01 \x01(\r\x12\x0f\n\x07product\x18\x02 \x01(\t\x12\x12\n\nquery_time\x18\x03 \x01(\x04\x12\x0e\n\x06random\x18\x04 \x03(\r\x12,\n\tuser_list\x18\x05 \x03(\x0b\x32\x19.test.OnlineUser.UserInfo\x1ay\n\x08UserInfo\x12\x0b\n\x03uid\x18\x01 \x01(\x04\x12\x11\n\tusre_name\x18\x02 \x01(\t\x12(\n\x04type\x18\x03 \x01(\x0e\x32\x1a.test.OnlineUser.PhoneType\x12\x11\n\tphone_num\x18\x04 \x01(\r\x12\x10\n\x08\x63li_type\x18\x05 \x01(\r\"+\n\tPhoneType\x12\n\n\x06MOBILE\x10\x00\x12\x08\n\x04HOME\x10\x01\x12\x08\n\x04WORK\x10\x02\x62\x06proto3')
)



_ONLINEUSER_PHONETYPE = _descriptor.EnumDescriptor(
  name='PhoneType',
  full_name='test.OnlineUser.PhoneType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='MOBILE', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='HOME', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WORK', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=290,
  serialized_end=333,
)
_sym_db.RegisterEnumDescriptor(_ONLINEUSER_PHONETYPE)


_ONLINEUSER_USERINFO = _descriptor.Descriptor(
  name='UserInfo',
  full_name='test.OnlineUser.UserInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uid', full_name='test.OnlineUser.UserInfo.uid', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='usre_name', full_name='test.OnlineUser.UserInfo.usre_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='test.OnlineUser.UserInfo.type', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='phone_num', full_name='test.OnlineUser.UserInfo.phone_num', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cli_type', full_name='test.OnlineUser.UserInfo.cli_type', index=4,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=167,
  serialized_end=288,
)

_ONLINEUSER = _descriptor.Descriptor(
  name='OnlineUser',
  full_name='test.OnlineUser',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='rsp_code', full_name='test.OnlineUser.rsp_code', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='product', full_name='test.OnlineUser.product', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='query_time', full_name='test.OnlineUser.query_time', index=2,
      number=3, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='random', full_name='test.OnlineUser.random', index=3,
      number=4, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='user_list', full_name='test.OnlineUser.user_list', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_ONLINEUSER_USERINFO, ],
  enum_types=[
    _ONLINEUSER_PHONETYPE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=36,
  serialized_end=333,
)

_ONLINEUSER_USERINFO.fields_by_name['type'].enum_type = _ONLINEUSER_PHONETYPE
_ONLINEUSER_USERINFO.containing_type = _ONLINEUSER
_ONLINEUSER.fields_by_name['user_list'].message_type = _ONLINEUSER_USERINFO
_ONLINEUSER_PHONETYPE.containing_type = _ONLINEUSER
DESCRIPTOR.message_types_by_name['OnlineUser'] = _ONLINEUSER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

OnlineUser = _reflection.GeneratedProtocolMessageType('OnlineUser', (_message.Message,), dict(

  UserInfo = _reflection.GeneratedProtocolMessageType('UserInfo', (_message.Message,), dict(
    DESCRIPTOR = _ONLINEUSER_USERINFO,
    __module__ = 'protos.python_proto_pb2'
    # @@protoc_insertion_point(class_scope:test.OnlineUser.UserInfo)
    ))
  ,
  DESCRIPTOR = _ONLINEUSER,
  __module__ = 'protos.python_proto_pb2'
  # @@protoc_insertion_point(class_scope:test.OnlineUser)
  ))
_sym_db.RegisterMessage(OnlineUser)
_sym_db.RegisterMessage(OnlineUser.UserInfo)


# @@protoc_insertion_point(module_scope)