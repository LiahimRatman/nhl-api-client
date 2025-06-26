#!/usr/bin/env python3
"""
NHL Schedule Analysis Example
=============================

This example demonstrates how to analyze NHL schedule data, including
game schedules, standings, and team performance trends.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nhl_api_client.client import NHLAPIClient
import pandas as pd
from datetime import datetime, timedelta
import json


def analyze_current_schedule(client):
    """
    Analyze today's NHL games
    """
    print("🗓️ Analyzing Today's NHL Schedule")
    print("-" * 40)
    
    # Get today's schedule
    today_schedule = client.get_schedule_now()
    
    if today_schedule and 'gameWeek' in today_schedule:
        games_today = []
        
        for day in today_schedule['gameWeek']:
            if day.get('games'):
                games_today.extend(day['games'])
        
        if games_today:
            print(f"📊 Games today: {len(games_today)}")
            
            for game in games_today:
                away_team = game['awayTeam']['placeName']['default']
                home_team = game['homeTeam']['placeName']['default']
                start_time = game.get('startTimeUTC', 'TBD')
                venue = game.get('venue', {}).get('default', 'Unknown')
                
                print(f"  🏒 {away_team} @ {home_team}")
                print(f"     📍 {venue}")
                print(f"     ⏰ {start_time}")
                
                # Check if game has started/finished
                if 'gameOutcome' in game:
                    outcome = game['gameOutcome']
                    print(f"     📊 Final Score: {outcome.get('lastPeriodType', 'Final')}")
                
                print()
        else:
            print("📅 No games scheduled for today")
    else:
        print("❌ Could not retrieve today's schedule")


def analyze_team_schedule(client, team_abbrev="TOR"):
    """
    Analyze a specific team's schedule
    """
    print(f"📋 Analyzing {team_abbrev} Schedule")
    print("-" * 40)
    
    # Get team schedule
    team_schedule = client.get_club_schedule(team_abbrev)
    
    if team_schedule and 'games' in team_schedule:
        games = team_schedule['games']
        print(f"📊 Total games in schedule: {len(games)}")
        
        # Analyze game statistics
        home_games = sum(1 for game in games if game.get('homeTeam', {}).get('abbrev') == team_abbrev)
        away_games = len(games) - home_games
        
        print(f"🏠 Home games: {home_games}")
        print(f"✈️ Away games: {away_games}")
        
        # Count wins/losses if available
        wins = losses = overtime_losses = 0
        total_goals_for = total_goals_against = 0
        
        completed_games = []
        upcoming_games = []
        
        for game in games:
            if game.get('gameOutcome'):
                completed_games.append(game)
                # This is a completed game
                if game.get('homeTeam', {}).get('abbrev') == team_abbrev:
                    # Home game
                    team_score = game.get('homeTeam', {}).get('score', 0)
                    opponent_score = game.get('awayTeam', {}).get('score', 0)
                else:
                    # Away game
                    team_score = game.get('awayTeam', {}).get('score', 0)
                    opponent_score = game.get('homeTeam', {}).get('score', 0)
                
                total_goals_for += team_score
                total_goals_against += opponent_score
                
                if team_score > opponent_score:
                    wins += 1
                elif 'OT' in game.get('gameOutcome', {}).get('lastPeriodType', '') or 'SO' in game.get('gameOutcome', {}).get('lastPeriodType', ''):
                    overtime_losses += 1
                else:
                    losses += 1
            else:
                upcoming_games.append(game)
        
        print(f"\n🏆 Record: {wins}-{losses}-{overtime_losses}")
        print(f"⚽ Goals For: {total_goals_for}")
        print(f"🥅 Goals Against: {total_goals_against}")
        print(f"📈 Goal Differential: {total_goals_for - total_goals_against:+d}")
        
        if completed_games:
            avg_gf = total_goals_for / len(completed_games)
            avg_ga = total_goals_against / len(completed_games)
            print(f"📊 Avg Goals For: {avg_gf:.2f}")
            print(f"📊 Avg Goals Against: {avg_ga:.2f}")
        
        # Show next few upcoming games
        print(f"\n📅 Next {min(5, len(upcoming_games))} games:")
        for game in upcoming_games[:5]:
            game_date = game.get('gameDate', 'TBD')
            if game.get('homeTeam', {}).get('abbrev') == team_abbrev:
                opponent = game.get('awayTeam', {}).get('abbrev', 'Unknown')
                location = "vs"
            else:
                opponent = game.get('homeTeam', {}).get('abbrev', 'Unknown')
                location = "@"
            
            print(f"  📆 {game_date}: {location} {opponent}")
    
    else:
        print("❌ Could not retrieve team schedule")


def analyze_standings(client):
    """
    Analyze current NHL standings
    """
    print("🏆 Current NHL Standings Analysis")
    print("-" * 40)
    
    standings = client.get_standings_now()
    
    if standings and 'standings' in standings:
        for conference in standings['standings']:
            conf_name = conference.get('conferenceName', 'Unknown Conference')
            print(f"\n🏒 {conf_name}")
            print("=" * len(conf_name))
            
            if 'divisions' in conference:
                for division in conference['divisions']:
                    div_name = division.get('divisionName', 'Unknown Division')
                    print(f"\n📊 {div_name}")
                    print("-" * len(div_name))
                    
                    if 'teams' in division:
                        teams = division['teams']
                        
                        # Sort teams by points (if available)
                        teams_sorted = sorted(teams, key=lambda x: x.get('points', 0), reverse=True)
                        
                        print(f"{'Rank':<4} {'Team':<20} {'GP':<3} {'W':<3} {'L':<3} {'OT':<3} {'PTS':<4} {'GF':<4} {'GA':<4} {'DIFF':<5}")
                        print("-" * 75)
                        
                        for i, team in enumerate(teams_sorted, 1):
                            team_name = team.get('teamName', {}).get('default', 'Unknown')[:18]
                            gp = team.get('gamesPlayed', 0)
                            wins = team.get('wins', 0)
                            losses = team.get('losses', 0)
                            ot_losses = team.get('otLosses', 0)
                            points = team.get('points', 0)
                            gf = team.get('goalFor', 0)
                            ga = team.get('goalAgainst', 0)
                            diff = gf - ga
                            
                            print(f"{i:<4} {team_name:<20} {gp:<3} {wins:<3} {losses:<3} {ot_losses:<3} {points:<4} {gf:<4} {ga:<4} {diff:+5}")
    else:
        print("❌ Could not retrieve standings")


def analyze_recent_games(client, team_abbrev="EDM", days_back=7):
    """
    Analyze recent games for a team
    """
    print(f"📈 Recent Performance Analysis ({team_abbrev} - Last {days_back} days)")
    print("-" * 60)
    
    # Get team schedule
    team_schedule = client.get_club_schedule(team_abbrev)
    
    if team_schedule and 'games' in team_schedule:
        games = team_schedule['games']
        
        # Filter recent completed games
        recent_games = []
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        for game in games:
            if game.get('gameOutcome'):  # Completed game
                game_date_str = game.get('gameDate', '')
                try:
                    game_date = datetime.strptime(game_date_str, '%Y-%m-%d')
                    if game_date >= cutoff_date:
                        recent_games.append(game)
                except ValueError:
                    continue
        
        if recent_games:
            print(f"🏒 Games played in last {days_back} days: {len(recent_games)}")
            
            wins = losses = ot_losses = 0
            total_gf = total_ga = 0
            
            print(f"\n{'Date':<12} {'Opponent':<15} {'Score':<15} {'Result':<10}")
            print("-" * 60)
            
            for game in sorted(recent_games, key=lambda x: x.get('gameDate', '')):
                game_date = game.get('gameDate', 'Unknown')
                
                if game.get('homeTeam', {}).get('abbrev') == team_abbrev:
                    # Home game
                    opponent = game.get('awayTeam', {}).get('abbrev', 'Unknown')
                    team_score = game.get('homeTeam', {}).get('score', 0)
                    opp_score = game.get('awayTeam', {}).get('score', 0)
                    venue = "vs"
                else:
                    # Away game
                    opponent = game.get('homeTeam', {}).get('abbrev', 'Unknown')
                    team_score = game.get('awayTeam', {}).get('score', 0)
                    opp_score = game.get('homeTeam', {}).get('score', 0)
                    venue = "@"
                
                total_gf += team_score
                total_ga += opp_score
                
                score_str = f"{team_score}-{opp_score}"
                
                if team_score > opp_score:
                    result = "W"
                    wins += 1
                elif 'OT' in game.get('gameOutcome', {}).get('lastPeriodType', '') or 'SO' in game.get('gameOutcome', {}).get('lastPeriodType', ''):
                    result = "OTL"
                    ot_losses += 1
                else:
                    result = "L"
                    losses += 1
                
                print(f"{game_date:<12} {venue} {opponent:<12} {score_str:<15} {result:<10}")
            
            print(f"\n📊 Recent Record: {wins}-{losses}-{ot_losses}")
            print(f"⚽ Goals For: {total_gf} ({total_gf/len(recent_games):.2f} per game)")
            print(f"🥅 Goals Against: {total_ga} ({total_ga/len(recent_games):.2f} per game)")
            print(f"📈 Goal Differential: {total_gf - total_ga:+d}")
        else:
            print(f"📅 No games found in the last {days_back} days")
    else:
        print("❌ Could not retrieve team schedule")


def main():
    """
    Run schedule analysis examples
    """
    print("📅 NHL Schedule Analysis Utility")
    print("=" * 50)
    print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Initialize client
    client = NHLAPIClient()
    
    try:
        # Analyze current schedule
        analyze_current_schedule(client)
        print()
        
        # Analyze specific team schedule
        analyze_team_schedule(client, "TOR")
        print()
        
        # Analyze standings
        analyze_standings(client)
        print()
        
        # Analyze recent performance
        analyze_recent_games(client, "EDM", days_back=14)
        
        print("\n" + "=" * 50)
        print("✅ Schedule analysis complete!")
        
    except Exception as e:
        print(f"❌ Analysis error: {e}")


if __name__ == "__main__":
    main() 