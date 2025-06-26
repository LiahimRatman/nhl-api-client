#!/usr/bin/env python3
"""
Example script demonstrating NHL API client usage for skater data extraction
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nhl_api_client.client import NHLAPIClient
import pandas as pd


def extract_skater_data_example():
    """Example of extracting skater data from NHL API"""
    
    # Initialize the client
    client = NHLAPIClient()
    
    print("=== NHL Skater Data Extraction Example ===\n")
    
    # Example 1: Get all teams
    print("1. Getting all NHL teams...")
    teams = client.get_teams()
    if 'teams' in teams:
        print(f"   Found {len(teams['teams'])} teams")
        for team in teams['teams'][:5]:  # Show first 5 teams
            print(f"   - {team['name']} (ID: {team['id']})")
        print("   ...\n")
    
    # Example 2: Get roster for a specific team (Toronto Maple Leafs - ID 10)
    print("2. Getting Toronto Maple Leafs roster...")
    maple_leafs_roster = client.get_team_roster(10)
    if 'roster' in maple_leafs_roster:
        skaters = [p for p in maple_leafs_roster['roster'] if p['position']['code'] != 'G']
        print(f"   Found {len(skaters)} skaters on the roster")
        for player in skaters[:3]:  # Show first 3 skaters
            print(f"   - {player['person']['fullName']} ({player['position']['code']})")
        print("   ...\n")
    
    # Example 3: Get stats for a specific player (Connor McDavid - ID 8478402)
    print("3. Getting Connor McDavid's stats...")
    mcdavid_stats = client.get_player_stats(8478402)
    if 'stats' in mcdavid_stats and len(mcdavid_stats['stats']) > 0:
        if 'splits' in mcdavid_stats['stats'][0] and len(mcdavid_stats['stats'][0]['splits']) > 0:
            stats = mcdavid_stats['stats'][0]['splits'][0]['stat']
            print(f"   Goals: {stats.get('goals', 'N/A')}")
            print(f"   Assists: {stats.get('assists', 'N/A')}")
            print(f"   Points: {stats.get('points', 'N/A')}")
            print(f"   Games Played: {stats.get('games', 'N/A')}\n")
    
    # Example 4: Search for players
    print("4. Searching for players named 'Crosby'...")
    crosby_players = client.search_player("Crosby")
    for player in crosby_players:
        print(f"   - {player['name']} - {player['team']} ({player['position']})")
    print()
    
    # Example 5: Get top scorers (limited to 5 for demo)
    print("5. Getting top 5 scorers (this may take a while as it fetches all team data)...")
    print("   Note: This is a comprehensive operation that fetches data from all teams")
    print("   In production, you might want to cache this data or run it periodically")
    
    # Uncomment the following lines if you want to run the full data extraction
    # This will take several minutes as it fetches data from all NHL teams
    """
    top_scorers = client.get_top_scorers(limit=5)
    if not top_scorers.empty:
        print("\n   Top 5 Scorers:")
        for idx, player in top_scorers.iterrows():
            print(f"   {idx+1}. {player['playerName']} ({player['team']}) - "
                  f"{player.get('goals', 0)}G, {player.get('assists', 0)}A, "
                  f"{player.get('points', 0)}P")
    """
    
    print("\n=== Example completed ===")
    print("\nTo run the full skater data extraction:")
    print("1. Uncomment the top_scorers section above")
    print("2. Or use: client.get_skater_stats_by_season() to get all skater data")
    print("3. Save the DataFrame using: df.to_csv('skater_stats.csv', index=False)")


def get_team_skater_stats_example():
    """Example of getting skater stats for a specific team"""
    
    client = NHLAPIClient()
    
    print("\n=== Team-Specific Skater Stats Example ===\n")
    
    # Get Edmonton Oilers (ID 22) skater stats
    print("Getting Edmonton Oilers skater stats...")
    
    roster = client.get_team_roster(22)  # Edmonton Oilers
    if 'roster' not in roster:
        print("Failed to get roster data")
        return
    
    skater_stats = []
    
    for player in roster['roster']:
        if player['position']['code'] != 'G':  # Skip goalies
            player_id = player['person']['id']
            player_name = player['person']['fullName']
            position = player['position']['code']
            
            # Get player stats
            stats_data = client.get_player_stats(player_id)
            
            if 'stats' in stats_data and len(stats_data['stats']) > 0:
                if 'splits' in stats_data['stats'][0] and len(stats_data['stats'][0]['splits']) > 0:
                    stats = stats_data['stats'][0]['splits'][0]['stat']
                    
                    skater_stats.append({
                        'Name': player_name,
                        'Position': position,
                        'Games': stats.get('games', 0),
                        'Goals': stats.get('goals', 0),
                        'Assists': stats.get('assists', 0),
                        'Points': stats.get('points', 0),
                        'PlusMinus': stats.get('plusMinus', 0),
                        'PIM': stats.get('pim', 0),
                        'Shots': stats.get('shots', 0),
                        'Hits': stats.get('hits', 0)
                    })
    
    # Convert to DataFrame and display
    if skater_stats:
        df = pd.DataFrame(skater_stats)
        df_sorted = df.sort_values('Points', ascending=False)
        
        print(f"\nEdmonton Oilers Skater Stats (Top 10 by Points):")
        print(df_sorted.head(10).to_string(index=False))
        
        # Save to CSV
        df_sorted.to_csv('nhl-data-parsing/oilers_skater_stats.csv', index=False)
        print(f"\nData saved to: oilers_skater_stats.csv")


if __name__ == "__main__":
    # Run the basic example
    extract_skater_data_example()
    
    # Run the team-specific example
    get_team_skater_stats_example() 