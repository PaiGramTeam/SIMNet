from simnet.client.components.auth_client.app import AppAuthClient
from simnet.client.components.auth_client.auth_ticket import AuthTicketAuthClient
from simnet.client.components.auth_client.cookie_token import CookieTokenAuthClient
from simnet.client.components.auth_client.game import GameAuthClient
from simnet.client.components.auth_client.game_token import GameTokenAuthClient
from simnet.client.components.auth_client.login_ticket import LoginTicketAuthClient
from simnet.client.components.auth_client.ltoken import LTokenAuthClient
from simnet.client.components.auth_client.stoken import StokenAuthClient


class AuthBaseClient(
    AppAuthClient,
    AuthTicketAuthClient,
    CookieTokenAuthClient,
    GameAuthClient,
    GameTokenAuthClient,
    LoginTicketAuthClient,
    LTokenAuthClient,
    StokenAuthClient,
):
    """Base client for AuthClient."""
