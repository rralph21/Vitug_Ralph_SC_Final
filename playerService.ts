// Hard coded sample data
/**
 * @param id - identifier of player
 * @param name - name of the player
 * @param wins - number of wins
 * @param losses - number of losses
 * @param totalScore - total accumilated score
 */

export interface Player {
    id: number;
    name: string;
    wins: number;
    losses: number;
    totalScore: number;

}

// sample players
const players: Player[] = [
    {id: 1, name: "ShadowStrike", wins: 15, losses: 5, totalScore: 28500},
    {id: 2, name: "NoobMaster", wins: 3, losses: 12, totalScore: 4200},
    {id: 3, name: "ProGamer99", wins: 0, losses: 0, totalScore: 0}

]

// ratings
export interface Ratings {
    id: number;
    name: string;
    rating: number;
    played: number;

}

/**
 * Single id player search
 * @param id - player id to search
 * @returns  - player if valid
 */

export function getPlayerStats(id: number): Player | undefined {
    for (let i = 0; i < players.length; i++) {
        const player = players[i];

        if (player.id === id) {
            return player;
        }
    }

    return undefined;
}

/**
 * Returns all players and the total count
 */
export function getAllPlayers(): { count: number; players: Player[] } {
  return {
    count: players.length,
    players: players
  };
}

