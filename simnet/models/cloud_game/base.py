from simnet.models.base import APIModel


class CloudGameCoin(APIModel):
    coin_num: int
    free_coin_num: int
    coin_limit: int
    exchange: int


class CloudGameFreeTime(APIModel):
    send_freetime: int
    free_time: int
    free_time_limit: int
    over_freetime: int


class CloudGameStatus(APIModel):
    status: int
    msg: str
    total_time_status: int
    status_new: int


class CloudGameStat(APIModel):
    vip_point: int


class CloudGamePlayCard(APIModel):
    expire: int
    msg: str
    short_msg: str
    play_card_limit: int
    remaining_sec: int
    play_card_tag: str


class CloudGameWallet(APIModel):
    coin: CloudGameCoin
    free_time: CloudGameFreeTime
    status: CloudGameStatus
    total_time: int
    stat: CloudGameStat
    play_card: CloudGamePlayCard
