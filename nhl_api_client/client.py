"""
NHL API Client for data extraction
Based on publicly available NHL API endpoints
Updated to use the current NHL API (api-web.nhle.com)
"""

import requests
import json
import pandas as pd
from typing import Dict, List, Optional, Union
from datetime import datetime, timedelta
import time


class NHLAPIClient:
    """Client for accessing NHL API data"""
    
    def __init__(self):
        self.base_url = "https://api-web.nhle.com/v1"
        self.stats_url = "https://api.nhle.com/stats/rest/en"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'NHL-Data-Parser/1.0'
        })
    
    def _make_request(self, url: str, params: Dict = None) -> Dict:
        """Make API request with error handling"""
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return {}

    # =============================================================================
    # SCHEDULE AND STANDINGS ENDPOINTS
    # =============================================================================
    
    def get_schedule_now(self) -> Dict:
        """Get today's schedule"""
        url = f"{self.base_url}/schedule/now"
        return self._make_request(url)
    
    def get_schedule_by_date(self, date: str) -> Dict:
        """
        Get schedule for a specific date
        
        Args:
            date: Date in YYYY-MM-DD format
        """
        url = f"{self.base_url}/schedule/{date}"
        return self._make_request(url)
    
    def get_club_schedule(self, team_abbrev: str, season: str = "now") -> Dict:
        """
        Get full season schedule for a team
        
        Args:
            team_abbrev: Team abbreviation (e.g., 'EDM', 'TOR')
            season: Season or 'now' for current season
        """
        url = f"{self.base_url}/club-schedule-season/{team_abbrev}/{season}"
        return self._make_request(url)
    
    def get_standings_now(self) -> Dict:
        """Get current standings"""
        url = f"{self.base_url}/standings/now"
        return self._make_request(url)
    
    def get_standings_by_date(self, date: str) -> Dict:
        """
        Get standings for a specific date
        
        Args:
            date: Date in YYYY-MM-DD format
        """
        url = f"{self.base_url}/standings/{date}"
        return self._make_request(url)

    # =============================================================================
    # GAME AND GAMECENTER ENDPOINTS
    # =============================================================================
    
    def get_gamecenter_boxscore(self, game_id: int) -> Dict:
        """
        Get game boxscore from gamecenter
        
        Args:
            game_id: NHL game ID
        """
        url = f"{self.base_url}/gamecenter/{game_id}/boxscore"
        return self._make_request(url)
    
    def get_gamecenter_play_by_play(self, game_id: int) -> Dict:
        """
        Get game play-by-play data
        
        Args:
            game_id: NHL game ID
        """
        url = f"{self.base_url}/gamecenter/{game_id}/play-by-play"
        return self._make_request(url)
    
    def get_player_game_log(self, player_id: int, season: str = "20232024", game_type: int = 2) -> Dict:
        """
        Get player's game log for a season
        
        Args:
            player_id: NHL player ID
            season: Season in format '20232024'
            game_type: Game type (2 = regular season, 3 = playoffs)
        """
        url = f"{self.base_url}/player/{player_id}/game-log/{season}/{game_type}"
        return self._make_request(url)

    # =============================================================================
    # ADDITIONAL SKATER STATS ENDPOINTS
    # =============================================================================
    
    def get_skater_shootout_stats(self, season: str = "20232024", limit: int = 100) -> pd.DataFrame:
        """
        Get skater shootout statistics
        
        Args:
            season: Season in format '20232024'
            limit: Maximum number of players to fetch
        """
        url = f"{self.stats_url}/skater/shootout"
        params = {
            'cayenneExp': f'seasonId={season}',
            'limit': limit,
            'start': 0
        }
        
        data = self._make_request(url, params)
        
        if 'data' not in data:
            print("Failed to get shootout data")
            return pd.DataFrame()
        
        df = pd.DataFrame(data['data'])
        if not df.empty:
            df['season'] = season
        
        return df
    
    def get_skater_timeonice_stats(self, season: str = "20232024", limit: int = 100) -> pd.DataFrame:
        """
        Get skater time on ice statistics
        
        Args:
            season: Season in format '20232024'
            limit: Maximum number of players to fetch
        """
        url = f"{self.stats_url}/skater/timeonice"
        params = {
            'cayenneExp': f'seasonId={season}',
            'limit': limit,
            'start': 0
        }
        
        data = self._make_request(url, params)
        
        if 'data' not in data:
            print("Failed to get time on ice data")
            return pd.DataFrame()
        
        df = pd.DataFrame(data['data'])
        if not df.empty:
            df['season'] = season
        
        return df
    
    def get_skater_penaltykill_stats(self, season: str = "20232024", limit: int = 100) -> pd.DataFrame:
        """
        Get skater penalty kill statistics
        
        Args:
            season: Season in format '20232024'
            limit: Maximum number of players to fetch
        """
        url = f"{self.stats_url}/skater/penaltykill"
        params = {
            'cayenneExp': f'seasonId={season}',
            'limit': limit,
            'start': 0
        }
        
        data = self._make_request(url, params)
        
        if 'data' not in data:
            print("Failed to get penalty kill data")
            return pd.DataFrame()
        
        df = pd.DataFrame(data['data'])
        if not df.empty:
            df['season'] = season
        
        return df
    
    def get_skater_puckpossessions_stats(self, season: str = "20232024", limit: int = 100) -> pd.DataFrame:
        """
        Get skater puck possession statistics
        
        Args:
            season: Season in format '20232024'
            limit: Maximum number of players to fetch
        """
        url = f"{self.stats_url}/skater/puckPossessions"
        params = {
            'cayenneExp': f'seasonId={season}',
            'limit': limit,
            'start': 0
        }
        
        data = self._make_request(url, params)
        
        if 'data' not in data:
            print("Failed to get puck possession data")
            return pd.DataFrame()
        
        df = pd.DataFrame(data['data'])
        if not df.empty:
            df['season'] = season
        
        return df
    
    def get_skater_summaryshooting_stats(self, season: str = "20232024", limit: int = 100) -> pd.DataFrame:
        """
        Get skater summary shooting statistics
        
        Args:
            season: Season in format '20232024'
            limit: Maximum number of players to fetch
        """
        url = f"{self.stats_url}/skater/summaryshooting"
        params = {
            'cayenneExp': f'seasonId={season}',
            'limit': limit,
            'start': 0
        }
        
        data = self._make_request(url, params)
        
        if 'data' not in data:
            print("Failed to get summary shooting data")
            return pd.DataFrame()
        
        df = pd.DataFrame(data['data'])
        if not df.empty:
            df['season'] = season
        
        return df
    
    def get_skater_percentages_stats(self, season: str = "20232024", limit: int = 100) -> pd.DataFrame:
        """
        Get skater percentages statistics
        
        Args:
            season: Season in format '20232024'
            limit: Maximum number of players to fetch
        """
        url = f"{self.stats_url}/skater/percentages"
        params = {
            'cayenneExp': f'seasonId={season}',
            'limit': limit,
            'start': 0
        }
        
        data = self._make_request(url, params)
        
        if 'data' not in data:
            print("Failed to get percentages data")
            return pd.DataFrame()
        
        df = pd.DataFrame(data['data'])
        if not df.empty:
            df['season'] = season
        
        return df
    
    def get_skater_faceoffwins_stats(self, season: str = "20232024", limit: int = 100) -> pd.DataFrame:
        """
        Get skater faceoff wins statistics
        
        Args:
            season: Season in format '20232024'
            limit: Maximum number of players to fetch
        """
        url = f"{self.stats_url}/skater/faceoffwins"
        params = {
            'cayenneExp': f'seasonId={season}',
            'limit': limit,
            'start': 0
        }
        
        data = self._make_request(url, params)
        
        if 'data' not in data:
            print("Failed to get faceoff wins data")
            return pd.DataFrame()
        
        df = pd.DataFrame(data['data'])
        if not df.empty:
            df['season'] = season
        
        return df

    def get_skater_bios(self, season: str = "20232024", limit: int = 100) -> pd.DataFrame:
        """
        Get skater biographical information
        
        Args:
            season: Season in format '20232024'
            limit: Maximum number of players to fetch
        """
        url = f"{self.stats_url}/skater/bios"
        params = {
            'cayenneExp': f'seasonId={season}',
            'limit': limit,
            'start': 0
        }
        
        data = self._make_request(url, params)
        
        if 'data' not in data:
            print("Failed to get skater bios data")
            return pd.DataFrame()
        
        df = pd.DataFrame(data['data'])
        if not df.empty:
            df['season'] = season
        
        return df

    # =============================================================================
    # GOALIE STATS ENDPOINTS
    # =============================================================================
    
    def get_goalie_bios(self, season: str = "20232024", limit: int = 100) -> pd.DataFrame:
        """
        Get goalie biographical information
        
        Args:
            season: Season in format '20232024'
            limit: Maximum number of goalies to fetch
        """
        url = f"{self.stats_url}/goalie/bios"
        params = {
            'cayenneExp': f'seasonId={season}',
            'limit': limit,
            'start': 0
        }
        
        data = self._make_request(url, params)
        
        if 'data' not in data:
            print("Failed to get goalie bios")
            return pd.DataFrame()
        
        df = pd.DataFrame(data['data'])
        if not df.empty:
            df['season'] = season
        
        return df
    
    def get_goalie_advanced_stats(self, season: str = "20232024", limit: int = 100) -> pd.DataFrame:
        """
        Get advanced goalie statistics
        
        Args:
            season: Season in format '20232024'
            limit: Maximum number of goalies to fetch
        """
        url = f"{self.stats_url}/goalie/advanced"
        params = {
            'cayenneExp': f'seasonId={season}',
            'limit': limit,
            'start': 0
        }
        
        data = self._make_request(url, params)
        
        if 'data' not in data:
            print("Failed to get advanced goalie data")
            return pd.DataFrame()
        
        df = pd.DataFrame(data['data'])
        if not df.empty:
            df['season'] = season
        
        return df
    
    def get_goalie_shootout_stats(self, season: str = "20232024", limit: int = 100) -> pd.DataFrame:
        """
        Get goalie shootout statistics
        
        Args:
            season: Season in format '20232024'
            limit: Maximum number of goalies to fetch
        """
        url = f"{self.stats_url}/goalie/shootout"
        params = {
            'cayenneExp': f'seasonId={season}',
            'limit': limit,
            'start': 0
        }
        
        data = self._make_request(url, params)
        
        if 'data' not in data:
            print("Failed to get goalie shootout data")
            return pd.DataFrame()
        
        df = pd.DataFrame(data['data'])
        if not df.empty:
            df['season'] = season
        
        return df
    
    def get_goalie_penaltyshots_stats(self, season: str = "20232024", limit: int = 100) -> pd.DataFrame:
        """
        Get goalie penalty shots statistics
        
        Args:
            season: Season in format '20232024'
            limit: Maximum number of goalies to fetch
        """
        url = f"{self.stats_url}/goalie/penaltyShots"
        params = {
            'cayenneExp': f'seasonId={season}',
            'limit': limit,
            'start': 0
        }
        
        data = self._make_request(url, params)
        
        if 'data' not in data:
            print("Failed to get penalty shots data")
            return pd.DataFrame()
        
        df = pd.DataFrame(data['data'])
        if not df.empty:
            df['season'] = season
        
        return df
    
    def get_goalie_saves_by_strength_stats(self, season: str = "20232024", limit: int = 100) -> pd.DataFrame:
        """
        Get goalie saves by strength statistics
        
        Args:
            season: Season in format '20232024'
            limit: Maximum number of goalies to fetch
        """
        url = f"{self.stats_url}/goalie/savesByStrength"
        params = {
            'cayenneExp': f'seasonId={season}',
            'limit': limit,
            'start': 0
        }
        
        data = self._make_request(url, params)
        
        if 'data' not in data:
            print("Failed to get saves by strength data")
            return pd.DataFrame()
        
        df = pd.DataFrame(data['data'])
        if not df.empty:
            df['season'] = season
        
        return df
    
    def get_goalie_started_vs_relieved_stats(self, season: str = "20232024", limit: int = 100) -> pd.DataFrame:
        """
        Get goalie started vs relieved statistics
        
        Args:
            season: Season in format '20232024'
            limit: Maximum number of goalies to fetch
        """
        url = f"{self.stats_url}/goalie/startedVsRelieved"
        params = {
            'cayenneExp': f'seasonId={season}',
            'limit': limit,
            'start': 0
        }
        
        data = self._make_request(url, params)
        
        if 'data' not in data:
            print("Failed to get started vs relieved data")
            return pd.DataFrame()
        
        df = pd.DataFrame(data['data'])
        if not df.empty:
            df['season'] = season
        
        return df

    # =============================================================================
    # TEAM STATS ENDPOINTS
    # =============================================================================
    
    def get_team_faceoff_percentages(self, season: str = "20232024") -> pd.DataFrame:
        """
        Get team faceoff percentage statistics
        
        Args:
            season: Season in format '20232024'
        """
        url = f"{self.stats_url}/team/faceoffpercentages"
        params = {
            'cayenneExp': f'seasonId={season}',
            'limit': 32,
            'start': 0
        }
        
        data = self._make_request(url, params)
        
        if 'data' not in data:
            print("Failed to get team faceoff percentages")
            return pd.DataFrame()
        
        df = pd.DataFrame(data['data'])
        if not df.empty:
            df['season'] = season
        
        return df
    
    def get_team_faceoff_wins(self, season: str = "20232024") -> pd.DataFrame:
        """
        Get team faceoff wins statistics
        
        Args:
            season: Season in format '20232024'
        """
        url = f"{self.stats_url}/team/faceoffwins"
        params = {
            'cayenneExp': f'seasonId={season}',
            'limit': 32,
            'start': 0
        }
        
        data = self._make_request(url, params)
        
        if 'data' not in data:
            print("Failed to get team faceoff wins")
            return pd.DataFrame()
        
        df = pd.DataFrame(data['data'])
        if not df.empty:
            df['season'] = season
        
        return df
    
    def get_team_penalties_stats(self, season: str = "20232024") -> pd.DataFrame:
        """
        Get team penalties statistics
        
        Args:
            season: Season in format '20232024'
        """
        url = f"{self.stats_url}/team/penalties"
        params = {
            'cayenneExp': f'seasonId={season}',
            'limit': 32,
            'start': 0
        }
        
        data = self._make_request(url, params)
        
        if 'data' not in data:
            print("Failed to get team penalties data")
            return pd.DataFrame()
        
        df = pd.DataFrame(data['data'])
        if not df.empty:
            df['season'] = season
        
        return df
    
    def get_team_penaltykill_stats(self, season: str = "20232024") -> pd.DataFrame:
        """
        Get team penalty kill statistics
        
        Args:
            season: Season in format '20232024'
        """
        url = f"{self.stats_url}/team/penaltykill"
        params = {
            'cayenneExp': f'seasonId={season}',
            'limit': 32,
            'start': 0
        }
        
        data = self._make_request(url, params)
        
        if 'data' not in data:
            print("Failed to get team penalty kill data")
            return pd.DataFrame()
        
        df = pd.DataFrame(data['data'])
        if not df.empty:
            df['season'] = season
        
        return df
    
    def get_team_powerplay_stats(self, season: str = "20232024") -> pd.DataFrame:
        """
        Get team power play statistics
        
        Args:
            season: Season in format '20232024'
        """
        url = f"{self.stats_url}/team/powerplay"
        params = {
            'cayenneExp': f'seasonId={season}',
            'limit': 32,
            'start': 0
        }
        
        data = self._make_request(url, params)
        
        if 'data' not in data:
            print("Failed to get team power play data")
            return pd.DataFrame()
        
        df = pd.DataFrame(data['data'])
        if not df.empty:
            df['season'] = season
        
        return df
    
    def get_team_realtime_stats(self, season: str = "20232024") -> pd.DataFrame:
        """
        Get team real-time statistics
        
        Args:
            season: Season in format '20232024'
        """
        url = f"{self.stats_url}/team/realtime"
        params = {
            'cayenneExp': f'seasonId={season}',
            'limit': 32,
            'start': 0
        }
        
        data = self._make_request(url, params)
        
        if 'data' not in data:
            print("Failed to get team real-time data")
            return pd.DataFrame()
        
        df = pd.DataFrame(data['data'])
        if not df.empty:
            df['season'] = season
        
        return df
    
    def get_team_shootout_stats(self, season: str = "20232024") -> pd.DataFrame:
        """
        Get team shootout statistics
        
        Args:
            season: Season in format '20232024'
        """
        url = f"{self.stats_url}/team/shootout"
        params = {
            'cayenneExp': f'seasonId={season}',
            'limit': 32,
            'start': 0
        }
        
        data = self._make_request(url, params)
        
        if 'data' not in data:
            print("Failed to get team shootout data")
            return pd.DataFrame()
        
        df = pd.DataFrame(data['data'])
        if not df.empty:
            df['season'] = season
        
        return df
    
    def get_team_summaryshooting_stats(self, season: str = "20232024") -> pd.DataFrame:
        """
        Get team summary shooting statistics
        
        Args:
            season: Season in format '20232024'
        """
        url = f"{self.stats_url}/team/summaryshooting"
        params = {
            'cayenneExp': f'seasonId={season}',
            'limit': 32,
            'start': 0
        }
        
        data = self._make_request(url, params)
        
        if 'data' not in data:
            print("Failed to get team summary shooting data")
            return pd.DataFrame()
        
        df = pd.DataFrame(data['data'])
        if not df.empty:
            df['season'] = season
        
        return df
    
    def get_team_percentages_stats(self, season: str = "20232024") -> pd.DataFrame:
        """
        Get team percentages statistics
        
        Args:
            season: Season in format '20232024'
        """
        url = f"{self.stats_url}/team/percentages"
        params = {
            'cayenneExp': f'seasonId={season}',
            'limit': 32,
            'start': 0
        }
        
        data = self._make_request(url, params)
        
        if 'data' not in data:
            print("Failed to get team percentages data")
            return pd.DataFrame()
        
        df = pd.DataFrame(data['data'])
        if not df.empty:
            df['season'] = season
        
        return df

    # =============================================================================
    # EXISTING METHODS (UNCHANGED)
    # =============================================================================
    
    def get_teams(self) -> Dict:
        """Get all NHL teams"""
        url = f"{self.stats_url}/team"
        return self._make_request(url)
    
    def get_team_roster(self, team_abbrev: str, season: str = "current") -> Dict:
        """
        Get team roster
        
        Args:
            team_abbrev: NHL team abbreviation (e.g., 'TOR', 'EDM', 'MTL')
            season: Season (default: 'current')
        """
        url = f"{self.base_url}/roster/{team_abbrev}/{season}"
        return self._make_request(url)
    
    def get_player_stats(self, player_id: int, season: str = "20232024") -> Dict:
        """
        Get player statistics
        
        Args:
            player_id: NHL player ID
            season: Season in format '20232024'
        """
        url = f"{self.base_url}/player/{player_id}/landing"
        return self._make_request(url)
    
    def get_player_season_stats(self, player_id: int, season: str = "20232024") -> Dict:
        """
        Get player season statistics from stats API
        
        Args:
            player_id: NHL player ID  
            season: Season in format '20232024'
        
        Returns:
            Dictionary with player season stats
        """
        url = f"{self.stats_url}/skater/summary"
        params = {
            'cayenneExp': f'playerId={player_id} and seasonId={season}'
        }
        return self._make_request(url, params)
    
    def get_player_realtime_stats(self, player_id: int, season: str = "20232024") -> Dict:
        """
        Get player real-time statistics (hits, blocks, giveaways, etc.)
        
        Args:
            player_id: NHL player ID  
            season: Season in format '20232024'
        
        Returns:
            Dictionary with player real-time stats
        """
        url = f"{self.stats_url}/skater/realtime"
        params = {
            'cayenneExp': f'playerId={player_id} and seasonId={season}'
        }
        return self._make_request(url, params)
    
    def get_player_bios(self, player_id: int, season: str = "20232024") -> Dict:
        """
        Get player biographical information
        
        Args:
            player_id: NHL player ID  
            season: Season in format '20232024'
        
        Returns:
            Dictionary with player bio info
        """
        url = f"{self.stats_url}/skater/bios"
        params = {
            'cayenneExp': f'playerId={player_id} and seasonId={season}'
        }
        return self._make_request(url, params)
    
    def get_player_powerplay_stats(self, player_id: int, season: str = "20232024") -> Dict:
        """
        Get player power play statistics
        
        Args:
            player_id: NHL player ID  
            season: Season in format '20232024'
        
        Returns:
            Dictionary with player power play stats
        """
        url = f"{self.stats_url}/skater/powerplay"
        params = {
            'cayenneExp': f'playerId={player_id} and seasonId={season}'
        }
        return self._make_request(url, params)
    
    def get_player_penalty_stats(self, player_id: int, season: str = "20232024") -> Dict:
        """
        Get player penalty statistics
        
        Args:
            player_id: NHL player ID  
            season: Season in format '20232024'
        
        Returns:
            Dictionary with player penalty stats
        """
        url = f"{self.stats_url}/skater/penalties"
        params = {
            'cayenneExp': f'playerId={player_id} and seasonId={season}'
        }
        return self._make_request(url, params)
    
    def get_player_faceoff_stats(self, player_id: int, season: str = "20232024") -> Dict:
        """
        Get player faceoff statistics
        
        Args:
            player_id: NHL player ID  
            season: Season in format '20232024'
        
        Returns:
            Dictionary with player faceoff stats
        """
        url = f"{self.stats_url}/skater/faceoffpercentages"
        params = {
            'cayenneExp': f'playerId={player_id} and seasonId={season}'
        }
        return self._make_request(url, params)
    
    def get_player_penaltykill_stats(self, player_id: int, season: str = "20232024") -> Dict:
        """
        Get player penalty kill statistics
        
        Args:
            player_id: NHL player ID  
            season: Season in format '20232024'
        
        Returns:
            Dictionary with player penalty kill stats
        """
        url = f"{self.stats_url}/skater/penaltykill"
        params = {
            'cayenneExp': f'playerId={player_id} and seasonId={season}'
        }
        return self._make_request(url, params)
    
    def get_player_shootout_stats(self, player_id: int, season: str = "20232024") -> Dict:
        """
        Get player shootout statistics
        
        Args:
            player_id: NHL player ID  
            season: Season in format '20232024'
        
        Returns:
            Dictionary with player shootout stats
        """
        url = f"{self.stats_url}/skater/shootout"
        params = {
            'cayenneExp': f'playerId={player_id} and seasonId={season}'
        }
        return self._make_request(url, params)
    
    def get_player_timeonice_stats(self, player_id: int, season: str = "20232024") -> Dict:
        """
        Get player time on ice statistics
        
        Args:
            player_id: NHL player ID  
            season: Season in format '20232024'
        
        Returns:
            Dictionary with player time on ice stats
        """
        url = f"{self.stats_url}/skater/timeonice"
        params = {
            'cayenneExp': f'playerId={player_id} and seasonId={season}'
        }
        return self._make_request(url, params)
    
    def get_comprehensive_player_stats(self, player_id: int, season: str = "20232024") -> Dict:
        """
        Get comprehensive player statistics from multiple endpoints
        
        Args:
            player_id: NHL player ID  
            season: Season in format '20232024'
        
        Returns:
            Dictionary with all available player stats
        """
        stats = {}
        
        # Get different types of stats
        endpoints = {
            'summary': self.get_player_season_stats,
            'realtime': self.get_player_realtime_stats,
            'bios': self.get_player_bios,
            'powerplay': self.get_player_powerplay_stats,
            'penalties': self.get_player_penalty_stats,
            'faceoffs': self.get_player_faceoff_stats,
            'penaltykill': self.get_player_penaltykill_stats,
            'shootout': self.get_player_shootout_stats,
            'timeonice': self.get_player_timeonice_stats
        }
        
        for stat_type, method in endpoints.items():
            try:
                result = method(player_id, season)
                if 'data' in result and result['data']:
                    stats[stat_type] = result['data'][0]
                else:
                    stats[stat_type] = {}
            except Exception as e:
                print(f"Failed to get {stat_type} for player {player_id}: {e}")
                stats[stat_type] = {}
        
        return stats
    
    def get_skater_stats_by_season(self, season: str = "20232024", limit: int = 2000) -> pd.DataFrame:
        """
        Get all skater statistics for a given season
        
        Args:
            season: Season in format '20232024'
            limit: Maximum number of players to fetch
        
        Returns:
            DataFrame with skater statistics
        """
        print(f"Fetching skater stats for season {season}...")
        
        all_data = []
        start = 0
        batch_size = 100  # API limit per request
        
        while len(all_data) < limit:
            url = f"{self.stats_url}/skater/summary"
            params = {
                'cayenneExp': f'seasonId={season}',
                'limit': min(batch_size, limit - len(all_data)),
                'start': start
            }
            
            data = self._make_request(url, params)
            
            if 'data' not in data or not data['data']:
                break
                
            all_data.extend(data['data'])
            
            # Check if we've got all available data
            total_available = data.get('total', 0)
            if len(all_data) >= total_available:
                break
                
            start += batch_size
        
        if not all_data:
            print("Failed to get skater data")
            return pd.DataFrame()
        
        # Convert to DataFrame
        df = pd.DataFrame(all_data)
        
        # Add season column
        if not df.empty:
            df['season'] = season
            print(f"Successfully retrieved {len(df)} skater records")
        
        return df
    
    def get_top_scorers(self, season: str = "20232024", limit: int = 50) -> pd.DataFrame:
        """
        Get top scorers for a season
        
        Args:
            season: Season in format '20232024'
            limit: Number of top scorers to return
        
        Returns:
            DataFrame with top scorers sorted by points
        """
        print(f"Fetching top {limit} scorers for season {season}...")
        
        url = f"{self.stats_url}/skater/summary"
        params = {
            'cayenneExp': f'seasonId={season}',
            'limit': limit,
            'start': 0,
            'sort': '[{"property":"points","direction":"DESC"}]'
        }
        
        data = self._make_request(url, params)
        
        if 'data' not in data:
            print("Failed to get top scorers data")
            return pd.DataFrame()
        
        df = pd.DataFrame(data['data'])
        if not df.empty:
            df['season'] = season
            print(f"Successfully retrieved top {len(df)} scorers")
        
        return df
    
    def get_team_stats(self, season: str = "20232024") -> pd.DataFrame:
        """Get team statistics for a season"""
        url = f"{self.stats_url}/team/summary"
        params = {
            'cayenneExp': f'seasonId={season}'
        }
        
        data = self._make_request(url, params)
        
        if 'data' not in data:
            print("Failed to get team data")
            return pd.DataFrame()
        
        return pd.DataFrame(data['data'])
    
    def get_player_career_stats(self, player_id: int) -> Dict:
        """Get career statistics for a player"""
        url = f"{self.base_url}/player/{player_id}/landing"
        return self._make_request(url)
    
    def get_game_stats(self, game_id: int) -> Dict:
        """Get statistics for a specific game"""
        url = f"{self.base_url}/gamecenter/{game_id}/boxscore"
        return self._make_request(url)
    
    def get_schedule(self, team_abbrev: str = None, date: str = None) -> Dict:
        """
        Get schedule
        
        Args:
            team_abbrev: Team abbreviation (optional)
            date: Date in YYYY-MM-DD format (optional, defaults to today)
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
            
        if team_abbrev:
            url = f"{self.base_url}/club-schedule/{team_abbrev}/week/{date}"
        else:
            url = f"{self.base_url}/schedule/{date}"
            
        return self._make_request(url)
    
    def search_player(self, name: str, limit: int = 500) -> List[Dict]:
        """
        Search for players by name
        
        Args:
            name: Player name to search for
            limit: Maximum number of records to search through
            
        Returns:
            List of matching players
        """
        # Get skaters and search through them
        skaters_df = self.get_skater_stats_by_season(limit=limit)
        
        if skaters_df.empty:
            return []
        
        matching_players = []
        name_lower = name.lower()
        
        for _, player in skaters_df.iterrows():
            # Handle different name formats from API
            first_name = player.get('firstName', '')
            last_name = player.get('lastName', '')
            
            # If names are dictionaries, get the default value
            if isinstance(first_name, dict):
                first_name = first_name.get('default', '')
            if isinstance(last_name, dict):
                last_name = last_name.get('default', '')
                
            player_name = f"{first_name} {last_name}".lower()
            
            if name_lower in player_name:
                matching_players.append({
                    'id': player.get('playerId'),
                    'name': f"{first_name} {last_name}",
                    'team': player.get('teamAbbrevs', ''),
                    'position': player.get('positionCode', ''),
                    'points': player.get('points', 0),
                    'goals': player.get('goals', 0),
                    'assists': player.get('assists', 0)
                })
        
        # Sort by points (descending)
        matching_players.sort(key=lambda x: x['points'], reverse=True)
        return matching_players
    
    def get_goalie_stats(self, season: str = "20232024", limit: int = 100) -> pd.DataFrame:
        """
        Get goalie statistics for a season
        
        Args:
            season: Season in format '20232024'
            limit: Maximum number of goalies to fetch
        
        Returns:
            DataFrame with goalie statistics
        """
        url = f"{self.stats_url}/goalie/summary"
        params = {
            'cayenneExp': f'seasonId={season}',
            'limit': limit,
            'start': 0
        }
        
        data = self._make_request(url, params)
        
        if 'data' not in data:
            print("Failed to get goalie data")
            return pd.DataFrame()
        
        df = pd.DataFrame(data['data'])
        if not df.empty:
            df['season'] = season
        
        return df
    
    def get_skater_realtime_stats(self, season: str = "20232024", limit: int = 100) -> pd.DataFrame:
        """
        Get real-time skater statistics for a season (hits, blocks, giveaways, etc.)
        
        Args:
            season: Season in format '20232024'
            limit: Maximum number of players to fetch
        
        Returns:
            DataFrame with real-time skater statistics
        """
        print(f"Fetching real-time skater stats for season {season}...")
        
        all_data = []
        start = 0
        batch_size = 100
        
        while len(all_data) < limit:
            url = f"{self.stats_url}/skater/realtime"
            params = {
                'cayenneExp': f'seasonId={season}',
                'limit': min(batch_size, limit - len(all_data)),
                'start': start
            }
            
            data = self._make_request(url, params)
            
            if 'data' not in data or not data['data']:
                break
                
            all_data.extend(data['data'])
            
            total_available = data.get('total', 0)
            if len(all_data) >= total_available:
                break
                
            start += batch_size
        
        if not all_data:
            print("Failed to get real-time skater data")
            return pd.DataFrame()
        
        df = pd.DataFrame(all_data)
        if not df.empty:
            df['season'] = season
            print(f"Successfully retrieved {len(df)} real-time skater records")
        
        return df
    
    def get_skater_powerplay_stats(self, season: str = "20232024", limit: int = 100) -> pd.DataFrame:
        """
        Get power play skater statistics for a season
        
        Args:
            season: Season in format '20232024'
            limit: Maximum number of players to fetch
        
        Returns:
            DataFrame with power play skater statistics
        """
        print(f"Fetching power play skater stats for season {season}...")
        
        url = f"{self.stats_url}/skater/powerplay"
        params = {
            'cayenneExp': f'seasonId={season}',
            'limit': limit,
            'start': 0
        }
        
        try:
            data = self._make_request(url, params)
            
            if 'data' not in data:
                print("Failed to get power play skater data")
                return pd.DataFrame()
            
            df = pd.DataFrame(data['data'])
            if not df.empty:
                df['season'] = season
                print(f"Successfully retrieved {len(df)} power play skater records")
            
            return df
        except Exception as e:
            print(f"Error fetching skater powerplay stats: {e}")
            return pd.DataFrame()
    
    def get_skater_penalty_stats(self, season: str = "20232024", limit: int = 100) -> pd.DataFrame:
        """
        Get penalty skater statistics for a season
        
        Args:
            season: Season in format '20232024'
            limit: Maximum number of players to fetch
        
        Returns:
            DataFrame with penalty skater statistics
        """
        print(f"Fetching penalty skater stats for season {season}...")
        
        url = f"{self.stats_url}/skater/penalties"
        params = {
            'cayenneExp': f'seasonId={season}',
            'limit': limit,
            'start': 0
        }
        
        try:
            data = self._make_request(url, params)
            
            if 'data' not in data:
                print("Failed to get penalty skater data")
                return pd.DataFrame()
            
            df = pd.DataFrame(data['data'])
            if not df.empty:
                df['season'] = season
                print(f"Successfully retrieved {len(df)} penalty skater records")
            
            return df
        except Exception as e:
            print(f"Error fetching skater penalty stats: {e}")
            return pd.DataFrame() 