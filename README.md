# NHL Stats API Client

A comprehensive Python client for accessing NHL statistics and data through various official NHL APIs. This library provides easy access to player stats, team information, schedules, standings, and more.

## Features

- 🏒 **Player Statistics**: Access comprehensive player stats including scoring, real-time, power play, penalty kill, and faceoff data
- 🥅 **Goalie Statistics**: Retrieve goalie stats, advanced metrics, and shootout performance
- 🏆 **Team Data**: Get team statistics, power play/penalty kill data, and faceoff percentages
- 📅 **Schedule & Standings**: Access current schedules, standings, and game information
- 🎯 **Advanced Analytics**: Built-in support for advanced statistical analysis
- 📊 **Data Export**: Export data to CSV and JSON formats
- 🚀 **Easy to Use**: Simple, intuitive API with comprehensive error handling

## Installation

### From PyPI

```bash
pip install nhl-stats-api-client
```

### From Source

```bash
git clone https://github.com/liahimratman/nhl-api-client.git
cd nhl-api-client
pip install -e .
```

### Requirements

- Python 3.8+
- pandas
- requests

## Quick Start

```python
from nhl_api_client import NHLAPIClient

# Initialize the client
client = NHLAPIClient()

# Get all NHL teams
teams = client.get_teams()
print(f"Found {len(teams['data'])} teams")

# Get player stats for Connor McDavid (2023-24 season)
player_stats = client.get_player_season_stats(8478402, "20232024")
print(f"Goals: {player_stats['goals']}, Assists: {player_stats['assists']}")

# Get current standings
standings = client.get_standings_now()

# Get today's schedule
schedule = client.get_schedule_now()

# Export top scorers to CSV
top_scorers = client.get_top_scorers("20232024", limit=50)
top_scorers.to_csv("top_scorers.csv", index=False)
```

## API Reference

### Team Information

```python
# Get all NHL teams
teams = client.get_teams()
print(f"Teams: {teams['data']}")

# Get team roster
roster = client.get_team_roster("TOR")  # Toronto Maple Leafs
```

### Player Statistics

#### Individual Player Methods

```python
# Get basic season stats for a player
stats = client.get_player_season_stats(player_id, season_id)

# Get real-time stats (hits, blocks, giveaways, etc.)
realtime = client.get_player_realtime_stats(player_id, season_id)

# Get biographical information
bio = client.get_player_bios(player_id)

# Get power play statistics
pp_stats = client.get_player_powerplay_stats(player_id, season_id)

# Get penalty statistics
penalty_stats = client.get_player_penalty_stats(player_id, season_id)

# Get faceoff statistics
faceoff_stats = client.get_player_faceoff_stats(player_id, season_id)

# Get penalty kill statistics
penaltykill_stats = client.get_player_penaltykill_stats(player_id, season_id)

# Get shootout statistics
shootout_stats = client.get_player_shootout_stats(player_id, season_id)

# Get time on ice statistics
timeonice_stats = client.get_player_timeonice_stats(player_id, season_id)

# Get comprehensive stats from multiple endpoints
all_stats = client.get_comprehensive_player_stats(player_id, season_id)
```

#### Bulk Player Data Methods

```python
# Get top scorers
top_scorers = client.get_top_scorers(season_id, limit=100)

# Get skater stats by category
summary_stats = client.get_skater_stats_by_season(season_id, limit=500)
realtime_stats = client.get_skater_realtime_stats(season_id, limit=500)
powerplay_stats = client.get_skater_powerplay_stats(season_id, limit=500)
penaltykill_stats = client.get_skater_penaltykill_stats(season_id, limit=500)
penalty_stats = client.get_skater_penalty_stats(season_id, limit=500)
faceoff_stats = client.get_skater_faceoff_stats(season_id, limit=500)
shootout_stats = client.get_skater_shootout_stats(season_id, limit=500)
timeonice_stats = client.get_skater_timeonice_stats(season_id, limit=500)
bios_stats = client.get_skater_bios(season_id, limit=500)
```

### Goalie Statistics

```python
# Get goalie summary stats
goalie_stats = client.get_goalie_stats(season_id, limit=100)

# Get advanced goalie stats
advanced_stats = client.get_goalie_advanced_stats(season_id, limit=100)

# Get goalie biographical information
goalie_bios = client.get_goalie_bios(season_id, limit=100)

# Get shootout statistics
shootout_stats = client.get_goalie_shootout_stats(season_id, limit=100)

# Get starts and wins data
starts_stats = client.get_goalie_starts_stats(season_id, limit=100)
```

### Team Statistics

```python
# Get team summary statistics
team_stats = client.get_team_stats(season_id)

# Get team power play stats
pp_stats = client.get_team_powerplay_stats(season_id)

# Get team penalty kill stats
pk_stats = client.get_team_penaltykill_stats(season_id)

# Get team faceoff percentages
faceoff_stats = client.get_team_faceoff_percentages(season_id)

# Get team real-time stats
realtime_stats = client.get_team_realtime_stats(season_id)

# Get penalty statistics
penalty_stats = client.get_team_penalty_stats(season_id)
```

### Schedule and Standings

```python
# Get current standings
standings = client.get_standings_now()

# Get today's schedule
today_schedule = client.get_schedule_now()

# Get schedule for a specific date
date_schedule = client.get_schedule_by_date("2024-01-15")

# Get team's full season schedule
team_schedule = client.get_club_schedule("TOR")  # Toronto Maple Leafs
```

### Game Data

```python
# Get game center data
game_data = client.get_gamecenter(game_id)

# Get play-by-play data
pbp_data = client.get_play_by_play(game_id)

# Get player game logs
game_log = client.get_player_game_log(player_id, season_id)
```

## Usage Examples

### Example 1: Player Analysis

```python
from nhl_api_client import NHLAPIClient

client = NHLAPIClient()

# Analyze Connor McDavid's 2023-24 season
mcdavid_id = 8478402
season = "20232024"

# Get comprehensive stats
stats = client.get_comprehensive_player_stats(mcdavid_id, season)

print(f"Goals: {stats['summary']['goals']}")
print(f"Assists: {stats['summary']['assists']}")
print(f"Points: {stats['summary']['points']}")
print(f"Hits: {stats['realtime']['hits']}")
print(f"Power Play Goals: {stats['powerplay']['powerPlayGoals']}")
print(f"Penalty Kill Time: {stats['penaltykill']['timeOnIcePerGame']}")
print(f"Shootout Attempts: {stats['shootout']['shootoutAttempts']}")
print(f"Time on Ice: {stats['timeonice']['timeOnIcePerGame']}")
```

### Example 2: Team Comparison

```python
# Compare team power play effectiveness
pp_stats = client.get_team_powerplay_stats("20232024")

# Sort by power play percentage
pp_stats_sorted = pp_stats.sort_values('powerPlayPct', ascending=False)

print("Top 5 Power Play Teams:")
print(pp_stats_sorted[['teamFullName', 'powerPlayPct', 'powerPlayGoals']].head())
```

### Example 3: Export Data

```python
# Export comprehensive player data to CSV and JSON
import pandas as pd

# Get various stats
summary = client.get_skater_stats_by_season("20232024", limit=500)
realtime = client.get_skater_realtime_stats("20232024", limit=500)
powerplay = client.get_skater_powerplay_stats("20232024", limit=500)

# Export to CSV
summary.to_csv('summary_stats.csv', index=False)
realtime.to_csv('realtime_stats.csv', index=False)
powerplay.to_csv('powerplay_stats.csv', index=False)

# Export to JSON
summary.to_json('summary_stats.json', orient='records')
```

### Example 4: Schedule Analysis

```python
# Analyze today's games
schedule = client.get_schedule_now()

if schedule and 'gameWeek' in schedule:
    for day in schedule['gameWeek']:
        if day.get('games'):
            for game in day['games']:
                away = game['awayTeam']['placeName']['default']
                home = game['homeTeam']['placeName']['default']
                print(f"{away} @ {home}")
```

### Example 5: Team Roster Analysis

```python
# Get all teams and their rosters
teams = client.get_teams()

for team in teams['data']:
    team_abbrev = team['triCode']
    team_name = team['fullName']
    
    print(f"\n{team_name} ({team_abbrev}) Roster:")
    roster = client.get_team_roster(team_abbrev)
    
    # Print forwards
    if 'forwards' in roster:
        print("  Forwards:")
        for player in roster['forwards'][:5]:  # First 5 forwards
            print(f"    {player['firstName']['default']} {player['lastName']['default']}")
```

## Season ID Format

Season IDs follow the format `YYYYYYYY` where the first four digits are the start year and the last four are the end year:

- `20232024` = 2023-24 season
- `20222023` = 2022-23 season
- `20212022` = 2021-22 season

## Player ID

Player IDs are unique NHL identifiers. You can find them:

1. From the NHL website URLs
2. Using the roster endpoints
3. From existing data exports

Example: Connor McDavid's ID is `8478402`

## Error Handling

The client includes comprehensive error handling:

```python
try:
    stats = client.get_player_season_stats(player_id, season_id)
except Exception as e:
    print(f"Error retrieving stats: {e}")
```

## Rate Limiting

The client respects NHL API rate limits. If you're making many requests, consider:

- Adding delays between requests
- Using bulk endpoints when available
- Caching frequently accessed data

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Make sure to:

1. Add tests for new functionality
2. Update documentation
3. Follow existing code style
4. Add examples for new features

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This library is not officially affiliated with the NHL. It provides access to publicly available NHL data through their APIs. Please use responsibly and in accordance with NHL's terms of service.

## Changelog

### Version 1.0.2
- Removed unnecessary main() function from library
- Fixed build process with correct configuration files
- Clean, reliable build process established
- Updated package name to `nhl-stats-api-client`
- Removed openpyxl dependency (no longer needed)

### Version 1.0.1
- Updated dependencies and configuration

### Version 1.0.0
- Initial release
- Complete player statistics support
- Goalie statistics
- Team statistics
- Schedule and standings
- Data export functionality
- Comprehensive examples

## Support

If you encounter any issues or have questions:

1. Check the [examples](examples/) directory
2. Open an issue on GitHub: https://github.com/liahimratman/nhl-api-client/issues
3. Read the API documentation above

## Acknowledgments

- NHL for providing public APIs
- The Python community for excellent libraries
- Contributors to the NHL API documentation project 