from typing import Optional

from simnet.models.base import APIModel, Field
from simnet.models.starrail.chronicle.base import PartialTime
from simnet.models.zzz.chronicle.challenge import ZZZChallengeBuddy, ZZZChallengeCharacter


class ZZZHadalBrief(APIModel):
    """Represents a brief summary of Hadal information.

    Attributes:
        cur_period_zone_layer_count (int): The current period zone layer count.
        score (int): The score achieved.
        rank_percent (int): The rank percentage.
        rating (str): The rating achieved.
        max_score (int): The maximum score achieved.
    """

    cur_period_zone_layer_count: int
    score: int
    rank_percent: int
    rating: str
    max_score: int

    battle_time: Optional[int] = None
    challenge_time: Optional[PartialTime] = None


class ZZZHadalBuffer(APIModel):
    """Represents a buffer in Hadal information.

    Attributes:
        title (str): The title of the buffer.
        text (str): The description or text of the buffer.
    """

    title: str
    text: str


class ZZZHadalInfoFourthLayerInfoDetail(APIModel):
    """Represents detailed information for the fourth layer in Hadal.

    Attributes:
        layer_id (int): The identifier of the layer.
        challenge_time (PartialTime): The time when the challenge was completed.
        avatar_list (list[ZZZChallengeCharacter]): The list of characters used in the challenge.
        buddy (Optional[ZZZChallengeBuddy]): The buddy assistant used in the challenge, if available.
    """

    layer_id: int
    challenge_time: Optional[PartialTime] = None
    avatar_list: list[ZZZChallengeCharacter]
    buddy: Optional[ZZZChallengeBuddy]

    battle_time: Optional[int] = None


class ZZZHadalInfoFourthLayerDetail(APIModel):
    """Details of the fourth layer in Hadal.

    Attributes:
        buffer (ZZZHadalBuffer): The buffer information.
        challenge_time (PartialTime): The time of the challenge.
        rating (str): The rating achieved.
        layer_challenge_info_list (list[ZZZHadalInfoFourthLayerInfoDetail]):
            The list of detailed information for each layer challenge.
    """

    buffer: ZZZHadalBuffer
    challenge_time: PartialTime
    rating: str
    layer_challenge_info_list: list[ZZZHadalInfoFourthLayerInfoDetail]


class ZZZHadalInfoFitfhLayerInfoDetail(ZZZHadalInfoFourthLayerInfoDetail):
    """Details of the fifth layer information in Hadal, extending the fourth layer details.

    Attributes:
        rating (str): The rating achieved.
        buffer (ZZZHadalBuffer): The buffer information.
        score (int): The score achieved.
        monster_pic (str): The picture of the monster.
        max_score (int): The maximum score achieved.
    """

    rating: str
    buffer: ZZZHadalBuffer
    score: int
    monster_pic: str
    max_score: int


class ZZZHadalInfoFitfhLayerDetail(APIModel):
    """Details of the fifth layer in Hadal.

    Attributes:
        layer_challenge_info_list (list[ZZZHadalInfoFitfhLayerInfoDetail]):
            The list of detailed information for each layer challenge.
    """

    layer_challenge_info_list: list[ZZZHadalInfoFitfhLayerInfoDetail]


class ZZZHadalInfoV2(APIModel):
    """Version 2 of Hadal information.

    Attributes:
        season (int): The season identifier.
        begin_time (Optional[PartialTime]): The start time of the Hadal season.
        end_time (Optional[PartialTime]): The end time of the Hadal season.
        pass_fifth_floor (bool): Whether the fifth floor was passed.
        brief (Optional[ZZZHadalBrief]): A brief summary of Hadal information.
        fitfh_layer_detail (Optional[ZZZHadalInfoFitfhLayerDetail]):
            Details of the fifth layer.
        fourth_layer_detail (Optional[ZZZHadalInfoFourthLayerDetail]):
            Details of the fourth layer.
    """

    season: int = Field(alias="zone_id")
    begin_time: Optional[PartialTime] = Field(None, alias="hadal_begin_time")
    end_time: Optional[PartialTime] = Field(None, alias="hadal_end_time")

    pass_fifth_floor: bool

    brief: Optional[ZZZHadalBrief]
    fitfh_layer_detail: Optional[ZZZHadalInfoFitfhLayerDetail]
    fourth_layer_detail: Optional[ZZZHadalInfoFourthLayerDetail]


class ZZZHadalInfo(APIModel):
    """Represents the overall Hadal information.

    Attributes:
        hadal_ver (str): The version of the Hadal information.
        hadal_info_v2 (ZZZHadalInfoV2): The version 2 Hadal information.
        nick_name (Optional[str]): The nickname of the player, if available.
        icon (Optional[str]): The icon of the player, if available.
    """

    hadal_ver: str
    hadal_info_v2: ZZZHadalInfoV2
    nick_name: Optional[str] = None
    icon: Optional[str] = None
