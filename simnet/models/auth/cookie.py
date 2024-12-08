from simnet.models.base import APIModel


class GameLoginResult(APIModel):
    """Game login result."""

    combo_id: str
    open_id: str
    combo_token: str
    heartbeat: bool
    account_type: int
