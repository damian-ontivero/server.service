import grpc

from st_server.shared.application.authorization import authorization_pb2 as pb2
from st_server.shared.application.authorization import (
    authorization_pb2_grpc as pb2_grpc,
)


class AuthorizationClient:
    """Authorization Client for the grpc server."""

    def __init__(self, host="localhost", port=4004):
        """Initialize the client."""
        self.host = host
        self.port = port
        self.channel = grpc.insecure_channel(f"{self.host}:{self.port}")

    def check_permission(self, subject, object, action):
        """Check if the user has the permission."""
        with self.channel as channel:
            stub = pb2_grpc.AuthorizationServiceStub(channel)
            request = pb2.CheckRequest(
                subject=subject, action=action, object=object
            )
            response = stub.CheckPermission(request)
            return response.allowed
