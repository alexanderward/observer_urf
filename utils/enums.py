from .base import BaseEnum


class Region(BaseEnum):
    NA1 = "NA1"
    EUN1 = "EUN1"
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


class Champions(BaseEnum):
    Aatrox = 266
    Ahri = 103
    Akali = 84
    Alistar = 12
    Amumu = 32
    Anivia = 34
    Annie = 1
    Ashe = 22
    AurelionSol = 136
    Azir = 268
    Bard = 432
    Blitzcrank = 53
    Brand = 63
    Braum = 201
    Caitlyn = 51
    Camille = 164
    Cassiopeia = 69
    ChoGath = 31
    Corki = 42
    Darius = 122
    Diana = 131
    DrMundo = 36
    Draven = 119
    Ekko = 245
    Elise = 60
    Evelynn = 28
    Ezreal = 81
    Fiddlesticks = 9
    Fiora = 114
    Fizz = 105
    Galio = 3
    Gangplank = 41
    Garen = 86
    Gnar = 150
    Gragas = 79
    Graves = 104
    Hecarim = 120
    Heimerdinger = 74
    Illaoi = 420
    Irelia = 39
    Ivern = 427
    Janna = 40
    JarvanIV = 59
    Jax = 24
    Jayce = 126
    Jhin = 202
    Jinx = 222
    Kalista = 429
    Karma = 43
    Karthus = 30
    Kassadin = 38
    Katarina = 55
    Kayle = 10
    Kayn = 141
    Kennen = 85
    KhaZix = 121
    Kindred = 203
    Kled = 240
    KogMaw = 96
    LeBlanc = 7
    LeeSin = 64
    Leona = 89
    Lissandra = 127
    Lucian = 236
    Lulu = 117
    Lux = 99
    Malphite = 54
    Malzahar = 90
    Maokai = 57
    MasterYi = 11
    MissFortune = 21
    Mordekaiser = 82
    Morgana = 25
    Nami = 267
    Nasus = 75
    Nautilus = 111
    Nidalee = 76
    Nocturne = 56
    Nunu = 20
    Olaf = 2
    Orianna = 61
    Ornn = 516
    Pantheon = 80
    Poppy = 78
    Quinn = 133
    Rakan = 497
    Rammus = 33
    RekSai = 421
    Renekton = 58
    Rengar = 107
    Riven = 92
    Rumble = 68
    Ryze = 13
    Sejuani = 113
    Shaco = 35
    Shen = 98
    Shyvana = 102
    Singed = 27
    Sion = 14
    Sivir = 15
    Skarner = 72
    Sona = 37
    Soraka = 16
    Swain = 50
    Syndra = 134
    TahmKench = 223
    Taliyah = 163
    Talon = 91
    Taric = 44
    Teemo = 17
    Thresh = 412
    Tristana = 18
    Trundle = 48
    Tryndamere = 23
    TwistedFate = 4
    Twitch = 29
    Udyr = 77
    Urgot = 6
    Varus = 110
    Vayne = 67
    Veigar = 45
    VelKoz = 161
    Vi = 254
    Viktor = 112
    Vladimir = 8
    Volibear = 106
    Warwick = 19
    Wukong = 62
    Xayah = 498
    Xerath = 101
    XinZhao = 5
    Yasuo = 157
    Yorick = 83
    Zac = 154
    Zed = 238
    Ziggs = 115
    Zilean = 26
    Zoe = 142
    Zyra = 143