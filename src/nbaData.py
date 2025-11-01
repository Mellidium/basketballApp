from nba_api.stats.endpoints import playergamelog, leagueleaders, playercareerstats, teamdashboardbyshootingsplits

def get_league_leaders(stat_category):
    """
    Return league leaders for a given stat category (e.g., 'PTS', 'REB', 'AST').
    See nba_api docs for valid stat_category values.
    Returns a list of dicts with player info and stat value.
    """
    try:
        leaders = leagueleaders.LeagueLeaders(stat_category_abbreviation=stat_category)
        df = leaders.get_data_frames()[0]
        return df.to_dict(orient='records')
    except Exception as e:
        print(f"Error fetching league leaders: {e}")
        return []

def get_player_career_stats(player_id, per_mode='PerGame'):
    """
    Return career stats for a given player ID.
    
    Args:
        player_id: NBA player ID
        per_mode: 'PerGame', 'Totals', or 'Per36' (default: 'PerGame')
    
    Returns:
        dict with keys:
            - 'season_totals_regular_season': list of dicts with season-by-season stats
            - 'career_totals_regular_season': list of dicts with career totals
            - 'season_totals_post_season': list of dicts with playoff stats by season
            - 'career_totals_post_season': list of dicts with career playoff totals
    """
    try:
        career = playercareerstats.PlayerCareerStats(player_id=player_id, per_mode36=per_mode)
        dfs = career.get_data_frames()
        
        # The endpoint returns multiple data frames:
        # [0] = SeasonTotalsRegularSeason
        # [1] = CareerTotalsRegularSeason
        # [2] = SeasonTotalsPostSeason
        # [3] = CareerTotalsPostSeason
        # [4] = SeasonTotalsAllStarSeason
        # [5] = CareerTotalsAllStarSeason
        # [6] = SeasonTotalsCollegeSeason
        # [7] = CareerTotalsCollegeSeason
        # [8] = SeasonRankingsRegularSeason
        # [9] = SeasonRankingsPostSeason
        
        return {
            'season_totals_regular_season': dfs[0].to_dict(orient='records') if len(dfs) > 0 and not dfs[0].empty else [],
            'career_totals_regular_season': dfs[1].to_dict(orient='records') if len(dfs) > 1 and not dfs[1].empty else [],
            'season_totals_post_season': dfs[2].to_dict(orient='records') if len(dfs) > 2 and not dfs[2].empty else [],
            'career_totals_post_season': dfs[3].to_dict(orient='records') if len(dfs) > 3 and not dfs[3].empty else []
        }
    except Exception as e:
        print(f"Error fetching career stats: {e}")
        return {
            'season_totals_regular_season': [],
            'career_totals_regular_season': [],
            'season_totals_post_season': [],
            'career_totals_post_season': []
        }
from nba_api.stats.static import players, teams

def get_active_players():
    """Return a list of active NBA players."""
    return players.get_active_players()

def get_player_id_by_name(name):
    """Return the player ID for a given player name (case-insensitive). Returns None if not found."""
    for player in players.get_active_players():
        if player['full_name'].lower() == name.lower():
            return player['id']
    return None

def get_nba_teams():
    """Return a list of all NBA teams."""
    return teams.get_teams()

def get_team_id_by_name(name):
    """Return the team ID for a given team name (case-insensitive). Returns None if not found."""
    for team in teams.get_teams():
        if team['full_name'].lower() == name.lower() or team['nickname'].lower() == name.lower():
            return team['id']
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

def get_team_shot_locations(team_id, season='2024-25'):
    """
    Return shot location data for a given team and season.
    
    Args:
        team_id: NBA team ID
        season: Season in format 'YYYY-YY' (e.g., '2024-25')
    
    Returns:
        dict with shot location data by area
    """
    try:
        shot_data = teamdashboardbyshootingsplits.TeamDashboardByShootingSplits(
            team_id=team_id,
            season=season,
            measure_type_detailed_defense='Base',
            per_mode_detailed='PerGame'
        )
        
        # Get the shot area data (index 1 contains shot area splits)
        dfs = shot_data.get_data_frames()
        
        # Available DataFrames:
        # [0] = OverallTeamDashboard
        # [1] = Shot5FTTeamDashboard
        # [2] = Shot8FTTeamDashboard  
        # [3] = ShotAreaTeamDashboard
        # [4] = AssistedShotTeamDashboard
        # [5] = ShotTypeSummaryTeamDashboard
        # [6] = ShotTypeTeamDashboard
        # [7] = AssistedByTeamDashboard
        
        return {
            'overall': dfs[0].to_dict(orient='records') if len(dfs) > 0 and not dfs[0].empty else [],
            'shot_5ft': dfs[1].to_dict(orient='records') if len(dfs) > 1 and not dfs[1].empty else [],
            'shot_8ft': dfs[2].to_dict(orient='records') if len(dfs) > 2 and not dfs[2].empty else [],
            'shot_area': dfs[3].to_dict(orient='records') if len(dfs) > 3 and not dfs[3].empty else [],
            'assisted_shot': dfs[4].to_dict(orient='records') if len(dfs) > 4 and not dfs[4].empty else [],
            'shot_type_summary': dfs[5].to_dict(orient='records') if len(dfs) > 5 and not dfs[5].empty else [],
            'shot_type': dfs[6].to_dict(orient='records') if len(dfs) > 6 and not dfs[6].empty else [],
            'assisted_by': dfs[7].to_dict(orient='records') if len(dfs) > 7 and not dfs[7].empty else []
        }
    except Exception as e:
        print(f"Error fetching team shot locations: {e}")
        return {
            'overall': [],
            'shot_5ft': [],
            'shot_8ft': [],
            'shot_area': [],
            'assisted_shot': [],
            'shot_type_summary': [],
            'shot_type': [],
            'assisted_by': []
        }
