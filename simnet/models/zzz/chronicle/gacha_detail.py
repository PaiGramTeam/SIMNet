from enum import Enum

from simnet.models.base import APIModel


class ZZZGachaDetailTicketType(str, Enum):
    """
    Represents the different types of gacha tickets in the ZZZ game.

    Attributes:
        RECHARGE_MONOCHROME: A ticket type for recharge monochrome gacha.
        POLYCHROME: A ticket type for polychrome gacha.
        ENCRYPTED_MASTER_TAPE: A ticket type for encrypted master tape gacha.
        MASTER_TAPE: A ticket type for master tape gacha.
        BOOPON: A ticket type for boopon gacha.
    """

    RECHARGE_MONOCHROME = "GACHA_TICKET_TYPE_RECHARGE_MONOCHROME"
    POLYCHROME = "GACHA_TICKET_TYPE_POLYCHROME"
    ENCRYPTED_MASTER_TAPE = "GACHA_TICKET_TYPE_ENCRYPTED_MASTER_TAPE"
    MASTER_TAPE = "GACHA_TICKET_TYPE_MASTER_TAPE"
    BOOPON = "GACHA_TICKET_TYPE_BOOPON"


class ZZZGachaDetailTicket(APIModel):
    """
    Represents a gacha ticket in the ZZZ game.

    Attributes:
        ticket_type (ZZZGachaDetailTicketType): The type of the gacha ticket.
        ticket_cnt (int): The count of this type of gacha ticket.
    """

    ticket_type: ZZZGachaDetailTicketType
    ticket_cnt: int


class ZZZGachaDetail(APIModel):
    """
    Represents the details of a gacha system in the ZZZ game.

    Attributes:
        tickets (list[ZZZGachaDetailTicket]): A list of gacha tickets with their types and counts.
        gacha_info_list (list[dict]): A list of dictionaries containing additional gacha information.
    """

    tickets: list[ZZZGachaDetailTicket]
    gacha_info_list: list[dict]

    def _find_ticket_cnt(self, ticket_type: "ZZZGachaDetailTicketType") -> int:
        for ticket in self.tickets:
            if ticket.ticket_type == ticket_type:
                return ticket.ticket_cnt
        return 0

    @property
    def recharge_monochrome_cnt(self) -> int:
        return self._find_ticket_cnt(ZZZGachaDetailTicketType.RECHARGE_MONOCHROME)

    @property
    def polychrome_cnt(self) -> int:
        return self._find_ticket_cnt(ZZZGachaDetailTicketType.POLYCHROME)

    @property
    def encrypted_master_tape_cnt(self) -> int:
        return self._find_ticket_cnt(ZZZGachaDetailTicketType.ENCRYPTED_MASTER_TAPE)

    @property
    def master_tape_cnt(self) -> int:
        return self._find_ticket_cnt(ZZZGachaDetailTicketType.MASTER_TAPE)

    @property
    def boopon_cnt(self) -> int:
        return self._find_ticket_cnt(ZZZGachaDetailTicketType.BOOPON)
