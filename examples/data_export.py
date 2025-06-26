#!/usr/bin/env python3
"""
NHL Data Export Example
=======================

This example demonstrates how to extract and export NHL data to various formats
including CSV, JSON, and Excel files for further analysis.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nhl_api_client.client import NHLAPIClient
import pandas as pd
import json
from datetime import datetime


def export_player_stats(client, season="20232024", output_dir="nhl_exports"):
    """
    Export comprehensive player statistics to multiple formats
    """
    print("📊 Exporting Player Statistics...")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Get different types of player stats
    print("  • Fetching skater summary stats...")
    skater_summary = client.get_skater_stats_by_season(season, limit=500)
    
    print("  • Fetching skater real-time stats...")
    skater_realtime = client.get_skater_realtime_stats(season, limit=500)
    
    print("  • Fetching power play stats...")
    skater_powerplay = client.get_skater_powerplay_stats(season, limit=500)
    
    # Export to CSV
    if not skater_summary.empty:
        summary_file = f"{output_dir}/skater_summary_{season}.csv"
        skater_summary.to_csv(summary_file, index=False)
        print(f"  ✓ Exported summary stats: {summary_file}")
    
    if not skater_realtime.empty:
        realtime_file = f"{output_dir}/skater_realtime_{season}.csv"
        skater_realtime.to_csv(realtime_file, index=False)
        print(f"  ✓ Exported real-time stats: {realtime_file}")
    
    if not skater_powerplay.empty:
        pp_file = f"{output_dir}/skater_powerplay_{season}.csv"
        skater_powerplay.to_csv(pp_file, index=False)
        print(f"  ✓ Exported power play stats: {pp_file}")
    
    # Create combined Excel file
    excel_file = f"{output_dir}/nhl_skater_stats_{season}.xlsx"
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        if not skater_summary.empty:
            skater_summary.to_excel(writer, sheet_name='Summary', index=False)
        if not skater_realtime.empty:
            skater_realtime.to_excel(writer, sheet_name='RealTime', index=False)
        if not skater_powerplay.empty:
            skater_powerplay.to_excel(writer, sheet_name='PowerPlay', index=False)
    
    print(f"  ✓ Exported combined Excel file: {excel_file}")


def export_goalie_stats(client, season="20232024", output_dir="nhl_exports"):
    """
    Export goalie statistics to files
    """
    print("🥅 Exporting Goalie Statistics...")
    
    # Get goalie stats
    print("  • Fetching goalie summary stats...")
    goalie_summary = client.get_goalie_stats(season, limit=100)
    
    print("  • Fetching goalie advanced stats...")
    goalie_advanced = client.get_goalie_advanced_stats(season, limit=100)
    
    print("  • Fetching goalie shootout stats...")
    goalie_shootout = client.get_goalie_shootout_stats(season, limit=100)
    
    # Export individual CSV files
    if not goalie_summary.empty:
        summary_file = f"{output_dir}/goalie_summary_{season}.csv"
        goalie_summary.to_csv(summary_file, index=False)
        print(f"  ✓ Exported goalie summary: {summary_file}")
    
    if not goalie_advanced.empty:
        advanced_file = f"{output_dir}/goalie_advanced_{season}.csv"
        goalie_advanced.to_csv(advanced_file, index=False)
        print(f"  ✓ Exported goalie advanced stats: {advanced_file}")
    
    # Create combined goalie Excel file
    excel_file = f"{output_dir}/nhl_goalie_stats_{season}.xlsx"
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        if not goalie_summary.empty:
            goalie_summary.to_excel(writer, sheet_name='Summary', index=False)
        if not goalie_advanced.empty:
            goalie_advanced.to_excel(writer, sheet_name='Advanced', index=False)
        if not goalie_shootout.empty:
            goalie_shootout.to_excel(writer, sheet_name='Shootout', index=False)
    
    print(f"  ✓ Exported goalie Excel file: {excel_file}")


def export_team_stats(client, season="20232024", output_dir="nhl_exports"):
    """
    Export team statistics to files
    """
    print("🏒 Exporting Team Statistics...")
    
    # Get various team stats
    team_stats = client.get_team_stats(season)
    team_powerplay = client.get_team_powerplay_stats(season)
    team_penaltykill = client.get_team_penaltykill_stats(season)
    team_faceoffs = client.get_team_faceoff_percentages(season)
    
    # Create comprehensive team stats Excel file
    excel_file = f"{output_dir}/nhl_team_stats_{season}.xlsx"
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        if not team_stats.empty:
            team_stats.to_excel(writer, sheet_name='Overall', index=False)
        if not team_powerplay.empty:
            team_powerplay.to_excel(writer, sheet_name='PowerPlay', index=False)
        if not team_penaltykill.empty:
            team_penaltykill.to_excel(writer, sheet_name='PenaltyKill', index=False)
        if not team_faceoffs.empty:
            team_faceoffs.to_excel(writer, sheet_name='Faceoffs', index=False)
    
    print(f"  ✓ Exported team stats: {excel_file}")


def export_schedule_data(client, team_abbrev="EDM", output_dir="nhl_exports"):
    """
    Export schedule and standings data
    """
    print("📅 Exporting Schedule & Standings...")
    
    # Get current standings
    standings = client.get_standings_now()
    
    # Get team schedule
    team_schedule = client.get_club_schedule(team_abbrev)
    
    # Export standings to JSON
    if standings:
        standings_file = f"{output_dir}/current_standings.json"
        with open(standings_file, 'w') as f:
            json.dump(standings, f, indent=2)
        print(f"  ✓ Exported standings: {standings_file}")
    
    # Export team schedule to JSON
    if team_schedule:
        schedule_file = f"{output_dir}/{team_abbrev}_schedule.json"
        with open(schedule_file, 'w') as f:
            json.dump(team_schedule, f, indent=2)
        print(f"  ✓ Exported {team_abbrev} schedule: {schedule_file}")


def export_top_performers(client, season="20232024", output_dir="nhl_exports"):
    """
    Export top performers in various categories
    """
    print("🌟 Exporting Top Performers...")
    
    # Get top scorers
    top_scorers = client.get_top_scorers(season, limit=50)
    
    # Get various statistical leaders
    time_on_ice = client.get_skater_timeonice_stats(season, limit=50)
    penalty_leaders = client.get_skater_penaltykill_stats(season, limit=50)
    shootout_leaders = client.get_skater_shootout_stats(season, limit=50)
    
    # Create top performers Excel file
    excel_file = f"{output_dir}/nhl_top_performers_{season}.xlsx"
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        if not top_scorers.empty:
            top_scorers.to_excel(writer, sheet_name='TopScorers', index=False)
        if not time_on_ice.empty:
            time_on_ice.to_excel(writer, sheet_name='TimeOnIce', index=False)
        if not penalty_leaders.empty:
            penalty_leaders.to_excel(writer, sheet_name='PenaltyKill', index=False)
        if not shootout_leaders.empty:
            shootout_leaders.to_excel(writer, sheet_name='Shootout', index=False)
    
    print(f"  ✓ Exported top performers: {excel_file}")


def create_summary_report(output_dir="nhl_exports"):
    """
    Create a summary report of all exported data
    """
    print("📋 Creating Export Summary Report...")
    
    summary_file = f"{output_dir}/export_summary.txt"
    
    with open(summary_file, 'w') as f:
        f.write("NHL Data Export Summary\n")
        f.write("=" * 30 + "\n")
        f.write(f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Output Directory: {output_dir}\n\n")
        
        f.write("Exported Files:\n")
        f.write("-" * 15 + "\n")
        
        # List all files in output directory
        for file in sorted(os.listdir(output_dir)):
            if file != "export_summary.txt":
                file_path = os.path.join(output_dir, file)
                file_size = os.path.getsize(file_path)
                f.write(f"• {file} ({file_size:,} bytes)\n")
        
        f.write("\nData Categories:\n")
        f.write("-" * 16 + "\n")
        f.write("• Player Statistics (Summary, Real-time, Power Play)\n")
        f.write("• Goalie Statistics (Summary, Advanced, Shootout)\n")
        f.write("• Team Statistics (Overall, Special Teams, Faceoffs)\n")
        f.write("• Schedule & Standings Data\n")
        f.write("• Top Performers Analysis\n")
        
        f.write("\nUsage Instructions:\n")
        f.write("-" * 19 + "\n")
        f.write("• CSV files can be imported into Excel, Google Sheets, or R/Python\n")
        f.write("• Excel files contain multiple sheets for different data categories\n")
        f.write("• JSON files contain raw API responses for custom processing\n")
    
    print(f"  ✓ Created summary report: {summary_file}")


def main():
    """
    Run data export examples
    """
    print("📦 NHL Data Export Utility")
    print("=" * 40)
    print(f"Starting export at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Initialize client
    client = NHLAPIClient()
    
    # Set output directory
    output_dir = f"nhl_exports_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        # Export different types of data
        export_player_stats(client, output_dir=output_dir)
        print()
        
        export_goalie_stats(client, output_dir=output_dir)
        print()
        
        export_team_stats(client, output_dir=output_dir)
        print()
        
        export_schedule_data(client, team_abbrev="TOR", output_dir=output_dir)
        print()
        
        export_top_performers(client, output_dir=output_dir)
        print()
        
        # Create summary report
        create_summary_report(output_dir)
        
        print("=" * 40)
        print(f"✅ Export complete! Files saved to: {output_dir}")
        print(f"📁 Total files created: {len(os.listdir(output_dir))}")
        
        # Calculate total size
        total_size = sum(
            os.path.getsize(os.path.join(output_dir, f)) 
            for f in os.listdir(output_dir)
        )
        print(f"💾 Total data exported: {total_size:,} bytes ({total_size/1024/1024:.2f} MB)")
        
    except Exception as e:
        print(f"❌ Export error: {e}")


if __name__ == "__main__":
    main() 