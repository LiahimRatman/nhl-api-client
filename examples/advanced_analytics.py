#!/usr/bin/env python3
"""
NHL Advanced Analytics Example
==============================

This example demonstrates advanced analytics capabilities using the NHL API client,
including team performance analysis, player comparisons, goalie analysis, and special teams effectiveness.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nhl_api_client.client import NHLAPIClient
import pandas as pd
import numpy as np
from datetime import datetime


def analyze_team_performance(client, season="20232024"):
    """
    Comprehensive team performance analysis
    """
    print("🏒 Advanced Team Performance Analysis")
    print("=" * 50)
    
    # Get team stats for multiple categories
    team_stats = client.get_team_stats(season)
    team_pp = client.get_team_powerplay_stats(season)
    team_pk = client.get_team_penaltykill_stats(season)
    team_realtime = client.get_team_realtime_stats(season)
    
    if not team_stats.empty:
        # Top scoring teams
        top_scoring = team_stats.nlargest(5, 'goalsFor')
        print("\n📊 Top 5 Scoring Teams:")
        for _, team in top_scoring.iterrows():
            team_name = team.get('teamFullName', 'Unknown')
            goals = team.get('goalsFor', 0)
            games = team.get('gamesPlayed', 1)
            gpg = goals / games if games > 0 else 0
            print(f"  {team_name}: {goals} goals ({gpg:.2f} per game)")
        
        # Best defensive teams
        best_defense = team_stats.nsmallest(5, 'goalsAgainst')
        print("\n🛡️ Top 5 Defensive Teams:")
        for _, team in best_defense.iterrows():
            team_name = team.get('teamFullName', 'Unknown')
            goals_against = team.get('goalsAgainst', 0)
            games = team.get('gamesPlayed', 1)
            gag = goals_against / games if games > 0 else 0
            print(f"  {team_name}: {goals_against} goals against ({gag:.2f} per game)")


def analyze_player_comparisons(client, players, season="20232024"):
    """
    Compare multiple players across different statistical categories
    """
    print("\n🥅 Player Comparison Analysis")
    print("=" * 50)
    
    player_data = []
    
    for player_name in players:
        # Search for player
        search_results = client.search_player(player_name, limit=100)
        if search_results:
            player = search_results[0]  # Take the first result
            player_id = player['id']
            
            # Get comprehensive stats
            stats = client.get_comprehensive_player_stats(player_id, season)
            
            if stats.get('summary'):
                summary = stats['summary']
                realtime = stats.get('realtime', {})
                powerplay = stats.get('powerplay', {})
                
                player_data.append({
                    'name': player['name'],
                    'team': player['team'],
                    'goals': summary.get('goals', 0),
                    'assists': summary.get('assists', 0),
                    'points': summary.get('points', 0),
                    'games': summary.get('gamesPlayed', 0),
                    'hits': realtime.get('hits', 0),
                    'blocks': realtime.get('blockedShots', 0),
                    'pp_goals': powerplay.get('powerPlayGoals', 0),
                    'pp_points': powerplay.get('powerPlayPoints', 0)
                })
    
    if player_data:
        df = pd.DataFrame(player_data)
        df['ppg'] = (df['points'] / df['games']).round(2)
        df['goals_per_game'] = (df['goals'] / df['games']).round(2)
        
        print("\n📈 Player Statistics Comparison:")
        print(df[['name', 'team', 'goals', 'assists', 'points', 'ppg', 'hits', 'pp_goals']].to_string(index=False))
        
        # Find statistical leaders
        print(f"\n🏆 Statistical Leaders:")
        print(f"  Points Leader: {df.loc[df['points'].idxmax(), 'name']} ({df['points'].max()} pts)")
        print(f"  Goals Leader: {df.loc[df['goals'].idxmax(), 'name']} ({df['goals'].max()} goals)")
        print(f"  PPG Leader: {df.loc[df['ppg'].idxmax(), 'name']} ({df['ppg'].max()} ppg)")
        print(f"  Hits Leader: {df.loc[df['hits'].idxmax(), 'name']} ({df['hits'].max()} hits)")


def analyze_goalie_performance(client, season="20232024", min_games=10):
    """
    Analyze goalie performance with advanced metrics
    """
    print("\n🥅 Goalie Performance Analysis")
    print("=" * 50)
    
    # Get goalie stats
    goalies = client.get_goalie_stats(season, limit=50)
    goalie_advanced = client.get_goalie_advanced_stats(season, limit=50)
    
    if not goalies.empty:
        # Filter goalies with minimum games
        qualified_goalies = goalies[goalies['gamesPlayed'] >= min_games].copy()
        
        if not qualified_goalies.empty:
            # Calculate advanced metrics
            qualified_goalies['save_pct'] = qualified_goalies['savePercentage']
            qualified_goalies['gaa'] = qualified_goalies['goalsAgainstAverage']
            
            # Sort by save percentage
            top_goalies = qualified_goalies.nlargest(10, 'save_pct')
            
            print(f"\n🌟 Top 10 Goalies (min {min_games} games):")
            for _, goalie in top_goalies.iterrows():
                name = f"{goalie.get('firstName', {}).get('default', '')} {goalie.get('lastName', {}).get('default', '')}"
                team = goalie.get('teamAbbrevs', 'UNK')
                games = goalie.get('gamesPlayed', 0)
                save_pct = goalie.get('save_pct', 0)
                gaa = goalie.get('gaa', 0)
                wins = goalie.get('wins', 0)
                
                print(f"  {name} ({team}): {save_pct:.3f} SV%, {gaa:.2f} GAA, {wins}W in {games}GP")


def analyze_special_teams(client, season="20232024"):
    """
    Analyze power play and penalty kill effectiveness
    """
    print("\n⚡ Special Teams Analysis")
    print("=" * 50)
    
    # Get team special teams stats
    team_pp = client.get_team_powerplay_stats(season)
    team_pk = client.get_team_penaltykill_stats(season)
    
    if not team_pp.empty and not team_pk.empty:
        # Merge PP and PK data
        special_teams = team_pp.merge(
            team_pk[['teamId', 'penaltyKillPct', 'shortHandedGoalsAgainst']], 
            on='teamId', 
            how='inner'
        )
        
        print("\n🔥 Power Play Leaders:")
        top_pp = special_teams.nlargest(5, 'powerPlayPct')
        for _, team in top_pp.iterrows():
            team_name = team.get('teamFullName', 'Unknown')
            pp_pct = team.get('powerPlayPct', 0)
            pp_goals = team.get('powerPlayGoals', 0)
            print(f"  {team_name}: {pp_pct:.1f}% ({pp_goals} goals)")
        
        print("\n🛡️ Penalty Kill Leaders:")
        top_pk = special_teams.nlargest(5, 'penaltyKillPct')
        for _, team in top_pk.iterrows():
            team_name = team.get('teamFullName', 'Unknown')
            pk_pct = team.get('penaltyKillPct', 0)
            sha_goals = team.get('shortHandedGoalsAgainst', 0)
            print(f"  {team_name}: {pk_pct:.1f}% ({sha_goals} goals against)")


def main():
    """
    Run advanced analytics examples
    """
    print("🏒 NHL Advanced Analytics Dashboard")
    print("=" * 60)
    print(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Initialize client
    client = NHLAPIClient()
    
    # Run different analyses
    try:
        # Team performance analysis
        analyze_team_performance(client)
        
        # Player comparisons
        players_to_compare = ["McDavid", "Pastrnak", "MacKinnon", "Draisaitl"]
        analyze_player_comparisons(client, players_to_compare)
        
        # Goalie analysis
        analyze_goalie_performance(client)
        
        # Special teams analysis
        analyze_special_teams(client)
        
        print("\n" + "=" * 60)
        print("✅ Advanced analytics complete!")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")


if __name__ == "__main__":
    main() 