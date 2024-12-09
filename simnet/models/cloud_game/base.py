from simnet.models.base import APIModel


class CloudGameCoin(APIModel):
    """
    Represents a cloud game coin containing various attributes related to the number of coins, free coins, coin limit, and exchange rate.

    Attributes:
        coin_num (int): The number of coins.
        free_coin_num (int): The number of free coins.
        coin_limit (int): The limit of coins.
        exchange (int): The exchange rate of coins.
    """

    coin_num: int
    free_coin_num: int
    coin_limit: int
    exchange: int


class CloudGameFreeTime(APIModel):
    """
    Represents the free time attributes of a cloud game.

    Attributes:
        send_freetime (int): The amount of free time sent.
        free_time (int): The total free time available.
        free_time_limit (int): The limit of free time.
        over_freetime (int): The amount of over free time.
    """

    send_freetime: int
    free_time: int
    free_time_limit: int
    over_freetime: int


class CloudGameStatus(APIModel):
    """
    Represents the status attributes of a cloud game.

    Attributes:
        status (int): The current status of the cloud game.
        msg (str): The message associated with the status.
        total_time_status (int): The total time status of the cloud game.
        status_new (int): The new status of the cloud game.
    """

    status: int
    msg: str
    total_time_status: int
    status_new: int


class CloudGameStat(APIModel):
    """
    Represents the statistics of a cloud game.

    Attributes:
        vip_point (int): The VIP points of the cloud game.
    """

    vip_point: int


class CloudGamePlayCard(APIModel):
    """
    Represents a cloud game play card containing various attributes related to its expiration, messages, limits, and remaining time.

    Attributes:
        expire (int): The expiration time of the play card.
        msg (str): The message associated with the play card.
        short_msg (str): The short message associated with the play card.
        play_card_limit (int): The limit of the play card.
        remaining_sec (int): The remaining seconds of the play card.
        play_card_tag (str): The tag of the play card.
    """

    expire: int
    msg: str
    short_msg: str
    play_card_limit: int
    remaining_sec: int
    play_card_tag: str


class CloudGameWallet(APIModel):
    """
    Represents a cloud game wallet containing various attributes related to coins, free time, status, total time, statistics, and play cards.

    Attributes:
        coin (CloudGameCoin): The coin information of the cloud game wallet.
        free_time (CloudGameFreeTime): The free time information of the cloud game wallet.
        status (CloudGameStatus): The status information of the cloud game wallet.
        total_time (int): The total time associated with the cloud game wallet.
        stat (CloudGameStat): The statistics of the cloud game wallet.
        play_card (CloudGamePlayCard): The play card information of the cloud game wallet.
    """

    coin: CloudGameCoin
    free_time: CloudGameFreeTime
    status: CloudGameStatus
    total_time: int
    stat: CloudGameStat
    play_card: CloudGamePlayCard
