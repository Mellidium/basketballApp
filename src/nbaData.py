from nba_api.stats.static import players

def get_active_players():
    """Return a list of active NBA players."""
    return players.get_active_players()
