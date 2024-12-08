from simnet.client.components.auth_client.app import AppAuthClient
from simnet.client.components.auth_client.game import GameAuthClient


class AuthBaseClient(
    AppAuthClient,
    GameAuthClient,
):
    """Base client for AuthClient."""
