# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: contract.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0e\x63ontract.proto\"&\n\x07Request\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07payload\x18\x02 \x01(\t\"*\n\x05\x45rror\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x0c\n\x04\x63ode\x18\x01 \x01(\x05\">\n\x08Response\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07payload\x18\x02 \x01(\t\x12\x15\n\x05\x45rror\x18\x03 \x01(\x0b\x32\x06.Errorb\x06proto3')

_REQUEST = DESCRIPTOR.message_types_by_name['Request']
_ERROR = DESCRIPTOR.message_types_by_name['Error']
_RESPONSE = DESCRIPTOR.message_types_by_name['Response']
Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), {
    'DESCRIPTOR': _REQUEST,
    '__module__': 'contract_pb2'
    # @@protoc_insertion_point(class_scope:Request)
})
_sym_db.RegisterMessage(Request)

Error = _reflection.GeneratedProtocolMessageType('Error', (_message.Message,), {
    'DESCRIPTOR': _ERROR,
    '__module__': 'contract_pb2'
    # @@protoc_insertion_point(class_scope:Error)
})
_sym_db.RegisterMessage(Error)

Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), {
    'DESCRIPTOR': _RESPONSE,
    '__module__': 'contract_pb2'
    # @@protoc_insertion_point(class_scope:Response)
})
_sym_db.RegisterMessage(Response)

if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _REQUEST._serialized_start = 18
    _REQUEST._serialized_end = 56
    _ERROR._serialized_start = 58
    _ERROR._serialized_end = 100
    _RESPONSE._serialized_start = 102
    _RESPONSE._serialized_end = 164
# @@protoc_insertion_point(module_scope)
