from .enums import Game, Region

APP_KEYS = {
    Game.GENSHIN: {
        Region.OVERSEAS: "6a4c78fe0356ba4673b8071127b28123",
        Region.CHINESE: "d0d3a7342df2026a70f650b907800111",
    },
    Game.STARRAIL: {
        Region.OVERSEAS: "d74818dabd4182d4fbac7f8df1622648",
        Region.CHINESE: "4650f3a396d34d576c3d65df26415394",
    },
    Game.HONKAI: {
        Region.OVERSEAS: "243187699ab762b682a2a2e50ba02285",
        Region.CHINESE: "0ebc517adb1b62c6b408df153331f9aa",
    },
    Game.ZZZ: {
        Region.OVERSEAS: "ff0f2776bf515d79d1f8ff1fb98b2a06",
        Region.CHINESE: "8844b676f3268c082a56021d9f47a206",
    },
}
"""App keys used for game login."""

APP_IDS = {
    Game.GENSHIN: {
        Region.OVERSEAS: "4",
        Region.CHINESE: "4",
    },
    Game.STARRAIL: {
        Region.OVERSEAS: "11",
        Region.CHINESE: "8",
    },
    Game.HONKAI: {
        Region.OVERSEAS: "8",
        Region.CHINESE: "1",
    },
    Game.ZZZ: {
        Region.OVERSEAS: "15",
        Region.CHINESE: "12",
    },
}
"""App IDs used for game login."""

GAME_BIZS = {
    Region.OVERSEAS: {
        Game.GENSHIN: "hk4e_global",
        Game.STARRAIL: "hkrpg_global",
        Game.HONKAI: "bh3_os",
        Game.ZZZ: "nap_global",
    },
    Region.CHINESE: {
        Game.GENSHIN: "hk4e_cn",
        Game.STARRAIL: "hkrpg_cn",
        Game.HONKAI: "bh3_cn",
        Game.ZZZ: "nap_cn",
    },
}
