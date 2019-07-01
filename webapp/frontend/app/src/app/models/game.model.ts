export interface Team{
    id: string,
    created_at: string,
    team_id: string,
    win_rate: string,
    game: string
}

export interface GameParticipants{
    id: string,
    created_at: string,
    summoner_name: string,
    region: string,
    champion: string,
    hot_streak: boolean,
    team: Team,
    league: string,
    win_rate: number,
    game: string,
}

export interface BannedChampions{
    id: string,
    created_at: string,
    champion: string,
    order: number,
    team: Team,
    game: string
}

export interface Game {
    id: string,
    created_at: string,
    game_type: string,
    region: string,
    league: string,
    teams: Team[],
    bannedChampions: BannedChampions[],
    gameParticipants: GameParticipants[]
}

export enum League {
    GRANDMASTER = "GRANDMASTER",
    CHALLENGER = "CHALLENGER",
    MASTER = "MASTER",
    DIAMOND = "DIAMOND",
    PLATINUM = "PLATINUM",
    GOLD = "GOLD",
    SILVER = "SILVER",
    BRONZE = "BRONZE",
    IRON = "IRON"
}