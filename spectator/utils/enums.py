from .base import BaseEnum


class Region(BaseEnum):
    NA1 = "NA1"
    # EUN1 = "EUN1"  # Disabled for now.  Can't connect for some reason
    EUW1 = "EUW1"
    KR = "KR"
    LA1 = "LA1"
    LA2 = "LA2"
    BR1 = "BR1"
    OC1 = "OC1"
    JP1 = "JP1"
    RU = "RU"
    TR1 = "TR1"


class MatchTypes(BaseEnum):
    RANKED_5V5_SOLO = 420
    RANKED_5V5_FLEX = 440
    NORMAL_5V5_BLIND_PICK = 430
    ARAM = 450
    RANKED_3V3_FLEX = 470
    NORMAL_3V3_BLIND_PICK = 460


class Leagues(BaseEnum):
    GRANDMASTER = "GRANDMASTER"
    CHALLENGER = "CHALLENGER"
    MASTER = "MASTER"
    DIAMOND = "DIAMOND"
    PLATINUM = "PLATINUM"
    GOLD = "GOLD"
    SILVER = "SILVER"
    BRONZE = "BRONZE"
    IRON = "IRON"


class SpectatorGrid(BaseEnum):
    NA1 = ("spectator.na.lol.riotgames.com", 80)
    EUW1 = ("spectator.euw1.lol.riotgames.com", 80)
    EUN1 = ("spectator.eu.lol.riotgames.com", 8088)
    JP1 = ("spectator.jp1.lol.riotgames.com", 80)
    KR = ("spectator.kr.lol.riotgames.com", 80)
    OC1 = ("spectator.oc1.lol.riotgames.com", 80)
    BR1 = ("spectator.br.lol.riotgames.com", 80)
    LA1 = ("spectator.la1.lol.riotgames.com", 80)
    LA2 = ("spectator.la2.lol.riotgames.com", 80)
    RU = ("spectator.ru.lol.riotgames.com", 80)
    TR1 = ("spectator.tr.lol.riotgames.com", 80)
    PBE1 = ("spectator.pbe1.lol.riotgames.com", 80)
