#!/usr/bin/env python3
import sys
import os
import json

# Make lib/ importable regardless of where this script is run from
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lib.parser import parse_session_file
from lib.aggregate import aggregate_usage
from lib.format import format_status_line

def main():
    payload = json.load(sys.stdin)
    transcript_path = payload.get("transcript_path")

    if not transcript_path or not os.path.exists(transcript_path):
        print("\U0001F4B0 Token Ledger: waiting for data...")
        return

    events = parse_session_file(transcript_path)
    results = aggregate_usage(events)

    if not results:
        print("\U0001F4B0 $0.00 this session")
        return

    print(format_status_line(results))

if __name__ == "__main__":
    main()
