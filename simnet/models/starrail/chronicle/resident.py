from typing import List, Optional

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


class StarRailResident(APIModel):
    """Starrail chronicle resident activity."""

    residents: List

    def find_resident(self, key: str) -> Optional[dict]:
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
