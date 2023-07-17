from typing import Dict, Any, Optional, List, Union
from urllib import parse

from simnet.client.base import BaseClient
from simnet.client.routes import YSULOG_URL
from simnet.models.genshin.transaction import BaseTransaction, TransactionKind, ItemTransaction, Transaction
from simnet.utils.lang import create_short_lang_code


class TransactionClient(BaseClient):
    """Transaction component."""

    async def request_transaction(
        self,
        endpoint: str,
        authkey: str,
        *,
        method: str = "GET",
        lang: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make a request towards the transaction log endpoint.

        Args:
            endpoint (str): The endpoint to make the request to.
            authkey (str): The authkey to use for the request.
            method (str, optional): The HTTP method to use. Defaults to "GET".
            lang (str, optional): The language to use for the request. Defaults to None.
            params (Dict[str, Any], optional): The parameters to use for the request. Defaults to None.
        """
        params = dict(params or {})

        base_url = YSULOG_URL.get_url(self.region)
        url = base_url / endpoint

        params["authkey_ver"] = 1
        params["sign_type"] = 2
        params["authkey"] = parse.unquote(authkey)
        params["lang"] = create_short_lang_code(lang or self.lang)

        return await self.request_lab(url, method=method, params=params)

    async def _get_transaction_page(
        self,
        end_id: int,
        kind: str,
        authkey: str,
        *,
        lang: Optional[str] = None,
    ) -> List[BaseTransaction]:
        """Get a single page of transactions.

        Args:
            end_id (int): The ID of the last transaction to get.
            kind (str): The kind of transaction to get.
            authkey (str): The authkey to use for the request.
            lang (str, optional): The language to use for the request. Defaults to None.
        """
        kind = TransactionKind(kind)
        endpoint = "Get" + kind.value.capitalize() + "Log"

        data = await self.request_transaction(
            endpoint,
            lang=lang,
            authkey=authkey,
            params=dict(end_id=end_id, size=20),
        )

        transactions: List[BaseTransaction] = []
        for trans in data["list"]:
            model = ItemTransaction if "name" in trans else Transaction
            transactions.append(model(**trans, kind=kind, lang=lang or self.lang))

        return transactions

    async def transaction_log(
        self,
        authkey: str,
        kind: Optional[Union[str, List[str]]] = None,
        *,
        limit: Optional[int] = None,
        lang: Optional[str] = None,
        end_id: int = 0,
    ) -> List[BaseTransaction]:
        """Get the transaction log of a user.

        Arg:
            authkey (str): The authkey to use for the request.
            kind (Union[str, List[str]], optional): The kind of transaction to get. Defaults to None.
            limit (int, optional): The maximum number of transactions to get. Defaults to None.
            lang (str, optional): The language to use for the request. Defaults to None.
            end_id (int, optional): The ID of the last transaction to get. Defaults to 0.
        """
        kinds = kind or ["primogem", "crystal", "resin", "artifact", "weapon"]

        if isinstance(kinds, str):
            kinds = [kinds]

        iterators: List[BaseTransaction] = []
        for value in kinds:
            iterator = await self._get_transaction_page(end_id, value, lang=lang, authkey=authkey)
            iterators.extend(iterator)

        return iterators[: min(len(iterators), limit)] if limit else iterators
