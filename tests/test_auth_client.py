from typing import TYPE_CHECKING

import pytest
import pytest_asyncio

from simnet.client.components.auth import AuthClient
from simnet.utils.enum_ import Region
from simnet.utils.player import recognize_genshin_server

if TYPE_CHECKING:
    from simnet.client.cookies import Cookies


@pytest_asyncio.fixture
async def auth_client(account_id: int, cookies: "Cookies"):
    async with AuthClient(
        cookies=cookies,
        account_id=account_id,
        region=Region.CHINESE,
    ) as client_instance:
        yield client_instance


@pytest.mark.asyncio
class TestAuthClient:
    @staticmethod
    async def test_get_hk4e_token_by_cookie_token(auth_client: "AuthClient", genshin_player_id: int):
        await auth_client.get_hk4e_token_by_cookie_token(
            "hk4e_cn", recognize_genshin_server(genshin_player_id), player_id=genshin_player_id
        )
        hk4e_token = auth_client.client.cookies.get("e_hk4e_token")
        assert hk4e_token is not None

    @staticmethod
    async def test_get_stoken_by_login_ticket(auth_client: "AuthClient", login_ticket: str, account_id: int):
        if login_ticket is None:
            pytest.skip("Test case test_get_stoken_by_login_ticket skipped: Parameter login_ticket is None")
        stoken = await auth_client.get_stoken_by_login_ticket(login_ticket, account_id)
        assert stoken is not None

    @staticmethod
    async def test_get_cookie_token_by_stoken(auth_client: "AuthClient", stoken: str, account_id: int):
        if stoken is None:
            pytest.skip("Test case test_get_cookie_token_by_stoken skipped: Parameter stoken is None")
        cookie_token = await auth_client.get_cookie_token_by_stoken(stoken, account_id)
        assert cookie_token is not None

    @staticmethod
    async def test_get_ltoken_by_stoken(auth_client: "AuthClient", stoken: str, account_id: int):
        if stoken is None:
            pytest.skip("Test case test_get_ltoken_by_stoken skipped: Parameter stoken is None")
        ltoken = await auth_client.get_ltoken_by_stoken(stoken, account_id)
        assert ltoken is not None

    @staticmethod
    async def test_get_authkey_by_stoken(stoken: str, account_id: int, genshin_player_id: int):
        if stoken is None:
            pytest.skip("Test case test_get_authkey_by_stoken skipped: Parameter stoken  is None")
        async with AuthClient(
            cookies={"stoken": stoken},
            player_id=genshin_player_id,
            account_id=account_id,
            region=Region.CHINESE,
        ) as client_instance:
            authkey = await client_instance.get_authkey_by_stoken(
                "hk4e_cn", recognize_genshin_server(genshin_player_id), "webview_gacha"
            )
        assert authkey is not None
