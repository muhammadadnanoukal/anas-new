# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import fire_zone_pb2 as fire__zone__pb2


class FireAlarmZoneStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Get = channel.unary_unary(
        '/fire_zone.FireAlarmZone/Get',
        request_serializer=fire__zone__pb2.GetRequest.SerializeToString,
        response_deserializer=fire__zone__pb2.GetResponse.FromString,
        )
    self.GetStatus = channel.unary_unary(
        '/fire_zone.FireAlarmZone/GetStatus',
        request_serializer=fire__zone__pb2.GetStatusRequest.SerializeToString,
        response_deserializer=fire__zone__pb2.GetStatusResponse.FromString,
        )
    self.Add = channel.unary_unary(
        '/fire_zone.FireAlarmZone/Add',
        request_serializer=fire__zone__pb2.AddRequest.SerializeToString,
        response_deserializer=fire__zone__pb2.AddResponse.FromString,
        )
    self.Delete = channel.unary_unary(
        '/fire_zone.FireAlarmZone/Delete',
        request_serializer=fire__zone__pb2.DeleteRequest.SerializeToString,
        response_deserializer=fire__zone__pb2.DeleteResponse.FromString,
        )
    self.DeleteAll = channel.unary_unary(
        '/fire_zone.FireAlarmZone/DeleteAll',
        request_serializer=fire__zone__pb2.DeleteAllRequest.SerializeToString,
        response_deserializer=fire__zone__pb2.DeleteAllResponse.FromString,
        )
    self.SetAlarm = channel.unary_unary(
        '/fire_zone.FireAlarmZone/SetAlarm',
        request_serializer=fire__zone__pb2.SetAlarmRequest.SerializeToString,
        response_deserializer=fire__zone__pb2.SetAlarmResponse.FromString,
        )


class FireAlarmZoneServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def Get(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetStatus(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Add(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Delete(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DeleteAll(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SetAlarm(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_FireAlarmZoneServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Get': grpc.unary_unary_rpc_method_handler(
          servicer.Get,
          request_deserializer=fire__zone__pb2.GetRequest.FromString,
          response_serializer=fire__zone__pb2.GetResponse.SerializeToString,
      ),
      'GetStatus': grpc.unary_unary_rpc_method_handler(
          servicer.GetStatus,
          request_deserializer=fire__zone__pb2.GetStatusRequest.FromString,
          response_serializer=fire__zone__pb2.GetStatusResponse.SerializeToString,
      ),
      'Add': grpc.unary_unary_rpc_method_handler(
          servicer.Add,
          request_deserializer=fire__zone__pb2.AddRequest.FromString,
          response_serializer=fire__zone__pb2.AddResponse.SerializeToString,
      ),
      'Delete': grpc.unary_unary_rpc_method_handler(
          servicer.Delete,
          request_deserializer=fire__zone__pb2.DeleteRequest.FromString,
          response_serializer=fire__zone__pb2.DeleteResponse.SerializeToString,
      ),
      'DeleteAll': grpc.unary_unary_rpc_method_handler(
          servicer.DeleteAll,
          request_deserializer=fire__zone__pb2.DeleteAllRequest.FromString,
          response_serializer=fire__zone__pb2.DeleteAllResponse.SerializeToString,
      ),
      'SetAlarm': grpc.unary_unary_rpc_method_handler(
          servicer.SetAlarm,
          request_deserializer=fire__zone__pb2.SetAlarmRequest.FromString,
          response_serializer=fire__zone__pb2.SetAlarmResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'fire_zone.FireAlarmZone', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
