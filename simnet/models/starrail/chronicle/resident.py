from typing import List, Optional, Dict

from simnet.models.base import APIModel


class StarRailResidentBase(APIModel):
    """StarRailResident Base Model"""

    exists_data: bool = True
    is_hot: bool
    strategy_link: str = ""


class StarRailResidentBoxingListItem(APIModel):
    """Resident Boxing List Item"""

    id: int
    name: str
    best: int


class StarRailResidentBoxing(APIModel):
    """Resident Boxing"""

    base: StarRailResidentBase
    list: List[StarRailResidentBoxingListItem]


class StarRailResidentMuseumInfo(APIModel):
    """Resident Museum Info"""

    current_exp: int
    max_exp: int
    exhibition_num: int
    total_exhibition: int
    director_num: int
    total_director: int
    phase: str


class StarRailResidentMuseum(APIModel):
    """Resident Museum"""

    base: StarRailResidentBase
    museum: StarRailResidentMuseumInfo


class StarRailCopperManInfoBasic(APIModel):
    """Copper Man Info Basic"""

    level: int
    accumulate: int
    cur_common_order: int
    max_common_order: int
    cur_customer_order: int
    max_customer_order: int
    cur_alley_event: int
    max_alley_event: int

    @property
    def common_order_process(self) -> float:
        """Get the common order process."""
        return 100.0 * self.cur_common_order / self.max_common_order

    @property
    def customer_order_process(self) -> float:
        """Get the customer order process."""
        return 100.0 * self.cur_customer_order / self.max_customer_order

    @property
    def alley_event_process(self) -> float:
        """Get the alley event process."""
        return 100.0 * self.cur_alley_event / self.max_alley_event


class StarRailCopperManInfoShop(APIModel):
    """Copper Man Info Shop"""

    id: int
    icon: str
    name: str
    is_unlock: bool


class StarRailCopperManInfo(APIModel):
    """Copper Man Info"""

    basic: StarRailCopperManInfoBasic
    shops: List[StarRailCopperManInfoShop]
    exists_data: bool


class StarRailCopperMan(APIModel):
    """Copper Man"""

    base: StarRailResidentBase
    info: StarRailCopperManInfo


class StarRailResident(APIModel):
    """Starrail chronicle resident activity."""

    residents: List

    def find_resident(self, key: str) -> Optional[Dict]:
        """Find a resident by key."""
        for resident in self.residents:
            if list(resident.keys())[0] == key:
                return resident[key]
        raise ValueError("No starrail resident found.")

    @property
    def museum(self) -> StarRailResidentMuseum:
        """Get the museum resident."""
        return StarRailResidentMuseum(**self.find_resident("museum"))

    @property
    def boxing(self) -> StarRailResidentBoxing:
        """Get the boxing resident."""
        return StarRailResidentBoxing(**self.find_resident("boxing"))

    @property
    def copper_man(self) -> StarRailCopperMan:
        """Get the copper man activity."""
        return StarRailCopperMan(**self.find_resident("copper_man"))
