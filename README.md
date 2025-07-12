# qbit_cleanup

A Python-based automation system cleaning up stalled downloads and old smaller torrents qBittorrent instance

## Features

- Deletes torrents older than 15 days and <= 5GB (unless tagged `movies`, `tv`, etc.)
- Removes stalled torrents in the `autobrr` category (only if not completed and not excluded)
- Recursively loops until all stale torrents are removed
- Optional log rotation, cron integration, and orphaned `.torrent` cleaner
- Script to use for cron jobs

## Setup

1. Clone this repo
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install qbittorrent-api
