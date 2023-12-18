import grpc

from st_server.shared.application.authorization import authorization_pb2 as pb2
from st_server.shared.application.authorization import (
    authorization_pb2_grpc as pb2_grpc,
)


class AuthorizationClient:
    """Authorization Client for the gRPC server."""

    def __init__(self, host="localhost", port=4004):
        self.host = host
        self.port = port
        self.channel = grpc.insecure_channel(f"{self.host}:{self.port}")

    def check_permission(self, subject, obj, action):
        """Checks if the user has the permission."""
        try:
            with self.channel as channel:
                stub = pb2_grpc.AuthorizationServiceStub(channel)
                request = pb2.CheckRequest(
                    subject=subject, action=action, object=obj
                )
                response = stub.CheckPermission(request)
                return response.allowed
        except grpc.RpcError as rpc_error:
            # Handle gRPC communication errors
            # Example: log the error or raise a custom exception
            print(f"gRPC error: {rpc_error}")
            return False
        except Exception as e:
            # Handle other potential exceptions
            print(f"An error occurred: {e}")
            return False
