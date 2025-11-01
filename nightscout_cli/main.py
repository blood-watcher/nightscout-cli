#!/usr/bin/env python3
"""
Nightscout CLI - Command line interface for Nightscout API
"""
import argparse
import requests
import json
import sys
import os
from datetime import datetime, timedelta

# Defaults - can be overridden by args or env vars
DEFAULT_API_SECRET = os.environ.get("NIGHTSCOUT_API_SECRET", "soilentgreenandblue")
DEFAULT_HOST = os.environ.get("NIGHTSCOUT_HOST", "127.0.0.1")
DEFAULT_PORT = os.environ.get("NIGHTSCOUT_PORT", "80")

def api_get(base_url, api_secret, endpoint, params=None):
    """Make authenticated GET request to Nightscout API"""
    headers = {"API-SECRET": api_secret}
    try:
        response = requests.get(f"{base_url}{endpoint}", headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def cmd_get(args):
    """Get the latest blood glucose reading"""
    base_url = f"http://{args.host}:{args.port}"
    entries = api_get(base_url, args.api_secret, "/api/v1/entries.json", params={"count": 1})
    
    if not entries:
        print("No data available")
        return
    
    entry = entries[0]
    # Format: timestamp value units direction
    timestamp = datetime.fromisoformat(entry['dateString'].replace('Z', '+00:00'))
    value = entry.get('sgv', 'N/A')
    units = entry.get('units', 'mg/dL')
    direction = entry.get('direction', '')
    
    print(f"{timestamp.isoformat()} {value} {units} {direction}")

def cmd_history(args):
    """Get historical glucose data"""
    base_url = f"http://{args.host}:{args.port}"
    
    # Calculate time range
    end_time = datetime.now() - timedelta(days=args.days_ago)
    start_time = end_time - timedelta(minutes=args.period)
    
    # Convert to milliseconds since epoch
    params = {
        "find[dateString][$gte]": start_time.isoformat() + 'Z',
        "find[dateString][$lte]": end_time.isoformat() + 'Z',
        "count": 10000  # Large number to get all entries
    }
    
    entries = api_get(base_url, args.api_secret, "/api/v1/entries.json", params=params)
    
    if args.jsonl:
        # Output as JSONL (one JSON object per line)
        for entry in entries:
            # Include timestamp, sgv, units
            output = {
                "timestamp": entry.get('dateString'),
                "sgv": entry.get('sgv'),
                "units": entry.get('units', 'mg/dL'),
                "direction": entry.get('direction', '')
            }
            print(json.dumps(output))
    else:
        # Human-readable output
        for entry in entries:
            timestamp = entry.get('dateString')
            value = entry.get('sgv', 'N/A')
            units = entry.get('units', 'mg/dL')
            print(f"{timestamp} {value} {units}")

def main():
    parser = argparse.ArgumentParser(
        description="Nightscout CLI - Command line interface for Nightscout API"
    )
    
    # Global arguments
    parser.add_argument('--host', default=DEFAULT_HOST,
                       help=f'Nightscout host (default: {DEFAULT_HOST}, or NIGHTSCOUT_HOST env var)')
    parser.add_argument('--port', default=DEFAULT_PORT,
                       help=f'Nightscout port (default: {DEFAULT_PORT}, or NIGHTSCOUT_PORT env var)')
    parser.add_argument('--api-secret', default=DEFAULT_API_SECRET,
                       help='API secret (default: from NIGHTSCOUT_API_SECRET env var)')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # get command
    parser_get = subparsers.add_parser('get', help='Get the latest blood glucose reading')
    parser_get.set_defaults(func=cmd_get)
    
    # history command
    parser_history = subparsers.add_parser('history', help='Get historical glucose data')
    parser_history.add_argument('--days-ago', type=int, default=0, 
                                help='Number of days ago to fetch data for (default: 0 = today)')
    parser_history.add_argument('--period', type=int, default=1440,
                                help='Period in minutes to fetch (default: 1440 = 24 hours)')
    parser_history.add_argument('--jsonl', action='store_true',
                                help='Output as JSONL (one JSON object per line)')
    parser_history.set_defaults(func=cmd_history)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)

if __name__ == '__main__':
    main()