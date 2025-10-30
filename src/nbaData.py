from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players

def get_active_players():
    """Return a list of active NBA players."""
    return players.get_active_players()

def get_player_id_by_name(name):
    """Return the player ID for a given player name (case-insensitive). Returns None if not found."""
    for player in players.get_active_players():
        if player['full_name'].lower() == name.lower():
            return player['id']
    return None

def get_most_recent_game_stats(player_id):
    """Return stats for the most recent game for the given player ID. Returns None if not found."""
    try:
        gamelog = playergamelog.PlayerGameLog(player_id=player_id, season='2025-26')
        df = gamelog.get_data_frames()[0]
        if not df.empty:
            return df.iloc[0].to_dict()
        else:
            return None
    except Exception as e:
        print(f"Error fetching game stats: {e}")
        return None
