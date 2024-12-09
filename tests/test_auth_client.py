from typing import TYPE_CHECKING

import pytest
import pytest_asyncio

from simnet.client.components.auth import AuthClient
from simnet.utils.enums import Game, Region
from simnet.utils.player import recognize_genshin_game_biz, recognize_genshin_server

if TYPE_CHECKING:
    from simnet.client.cookies import Cookies


@pytest_asyncio.fixture
async def auth_client(region: "Region", cookies: "Cookies"):
    async with AuthClient(
        cookies=cookies,
        region=region,
    ) as client_instance:
        yield client_instance


@pytest.mark.asyncio
class TestAuthClient:
    @staticmethod
    async def test_get_hk4e_token_by_cookie_token(auth_client: "AuthClient", genshin_player_id: int):
        if genshin_player_id is None:
            pytest.skip("Test case test_get_hk4e_token_by_cookie_token skipped: No genshin player id set.")
        game_biz = recognize_genshin_game_biz(genshin_player_id)
        await auth_client.get_hk4e_token_by_cookie_token(
            game_biz, recognize_genshin_server(genshin_player_id), player_id=genshin_player_id
        )
        hk4e_token = auth_client.client.cookies.get("e_hk4e_token")
        assert hk4e_token is not None

    @staticmethod
    async def test_get_stoken_by_login_ticket(auth_client: "AuthClient", login_ticket: str, account_id: int):
        if auth_client.region != Region.CHINESE:
            pytest.skip(
                "Test case test_get_stoken_by_login_ticket skipped:"
                "This method is only available for the Chinese region."
            )
        if login_ticket is None:
            pytest.skip("Test case test_get_stoken_by_login_ticket skipped: Parameter login_ticket is None")
        stoken = await auth_client.get_stoken_by_login_ticket(login_ticket, account_id)
        assert stoken is not None

    @staticmethod
    async def test_get_cookie_token_by_stoken(auth_client: "AuthClient"):
        if auth_client.region != Region.CHINESE:
            pytest.skip(
                "Test case test_get_cookie_token_by_stoken skipped:"
                "This method is only available for the Chinese region."
            )
        if auth_client.cookies.get("stoken") is None:
            pytest.skip("Test case test_get_cookie_token_by_stoken skipped: stoken is None")
        cookie_token = await auth_client.get_cookie_token_by_stoken()
        assert cookie_token is not None

    @staticmethod
    async def test_get_ltoken_by_stoken(auth_client: "AuthClient"):
        if auth_client.region != Region.CHINESE:
            pytest.skip(
                "Test case test_get_ltoken_by_stoken skipped:This method is only available for the Chinese region."
            )
        if auth_client.cookies.get("stoken") is None:
            pytest.skip("Test case test_get_ltoken_by_stoken skipped: stoken is None")
        ltoken = await auth_client.get_ltoken_by_stoken()
        assert ltoken is not None

    @staticmethod
    async def test_get_authkey_by_stoken(auth_client: "AuthClient", region: "Region", genshin_player_id: int):
        if region != Region.CHINESE:
            pytest.skip(
                "Test case test_get_authkey_by_stoken skipped:This method is only available for the Chinese region."
            )
        if auth_client.cookies.get("stoken") is None:
            pytest.skip("Test case test_get_authkey_by_stoken skipped: stoken is None")
        async with AuthClient(
            cookies=auth_client.cookies,
            player_id=genshin_player_id,
            region=region,
        ) as client_instance:
            client_instance.game = Game.GENSHIN
            authkey = await client_instance.get_authkey_by_stoken("webview_gacha")
        assert authkey is not None

    @staticmethod
    async def test_get_stoken_v2_and_mid_by_by_stoken(auth_client: "AuthClient", region: "Region"):
        if region != Region.CHINESE:
            pytest.skip(
                "Test case test_get_authkey_by_stoken skipped:This method is only available for the Chinese region."
            )
        if auth_client.cookies.get("stoken") is None:
            pytest.skip("Test case test_get_authkey_by_stoken skipped: stoken is None")
        async with AuthClient(
            cookies=auth_client.cookies,
            region=region,
        ) as client_instance:
            s2, mid = await client_instance.get_stoken_v2_and_mid_by_by_stoken()
            assert s2
            assert mid

    @staticmethod
    async def test_verify_cookie_token(auth_client: "AuthClient"):
        if auth_client.cookies.get("cookie_token") is None:
            pytest.skip("Test case test_verify_cookie_token skipped: cookie_token is None")
        await auth_client.verify_cookie_token()
        assert True

    @staticmethod
    async def test_verify_ltoken(auth_client: "AuthClient"):
        if auth_client.cookies.get("ltoken") is None:
            pytest.skip("Test case test_verify_ltoken skipped: ltoken is None")
        await auth_client.verify_ltoken()
        assert True

    @staticmethod
    async def test_verify_stoken(auth_client: "AuthClient"):
        if auth_client.cookies.get("stoken") is None:
            pytest.skip("Test case test_verify_stoken skipped: stoken is None")
        await auth_client.verify_stoken()
        assert True
