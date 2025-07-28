#!/usr/bin/env python3

"""
qBittorrent Cleanup Script with Modes
Usage:
  python3 qbit_cleanup.py --mode autobrr       # every 5 min
  python3 qbit_cleanup.py --mode aged          # every 24 hrs
  python3 qbit_cleanup.py --mode dedupe        # optionally for deduplication
  Add --dry-run to preview deletions
"""

import os
import time
import argparse
import logging
from qbittorrentapi import Client, LoginFailed
from collections import defaultdict
from dotenv import load_dotenv

# === Parse CLI arguments ===
parser = argparse.ArgumentParser(description="qBittorrent Cleanup Script")
parser.add_argument("--mode", choices=["autobrr", "aged", "dedupe"], required=True)
parser.add_argument("--dry-run", action="store_true", help="Preview deletions only")
args = parser.parse_args()

# === Configuration ===
load_dotenv()
QBT_HOST = os.getenv("QBT_HOST")
QBT_PORT = int(os.getenv("QBT_PORT"))
QBT_USERNAME = os.getenv("QBT_USERNAME")
QBT_PASSWORD = os.getenv("QBT_PASSWORD")

EXCLUDED_TAGS = ["movies", "tv"]
NAME_EXCLUSIONS = ["nsw", "ebook"]
CROSSSEED_TAG = "cross-seed"

DAYS_THRESHOLD = 15
SIZE_THRESHOLD_GB = 5
AGE_THRESHOLD_SEC = DAYS_THRESHOLD * 86400
SIZE_THRESHOLD_BYTES = SIZE_THRESHOLD_GB * 1024 ** 3

log_file = f"cleanup-{args.mode}.log"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# === Connect to qBittorrent ===
try:
    qbt = Client(host=f"http://{QBT_HOST}:{QBT_PORT}/", username=QBT_USERNAME, password=QBT_PASSWORD)
    qbt.auth_log_in()
except LoginFailed:
    print("❌ Failed to log in to qBittorrent. Check credentials.")
    exit(1)

torrents = qbt.torrents_info()
now = int(time.time())

def log_and_print(message):
    print(message)
    logging.info(message)

# === Mode: Dedupe ===
if args.mode == "dedupe":
    log_and_print(f"\n📦 Total torrents found: {len(torrents)}")
    log_and_print(f"🚀 Running in mode: dedupe{' (DRY RUN)' if args.dry_run else ''}\n")

    movie_groups = defaultdict(list)
    total_removed = 0

    for torrent in torrents:
        if torrent.category.lower() != "movies":
            continue
        base_name = torrent.name.split(" (")[0].strip().lower()
        movie_groups[base_name].append(torrent)

    for base_name, group in movie_groups.items():
        if len(group) <= 1:
            continue

        # Skip group if all have excluded name patterns or tags
        group_filtered = []
        for torrent in group:
            tags = [t.strip().lower() for t in torrent.tags.split(",")] if torrent.tags else []
            name_lower = torrent.name.lower()

            if CROSSSEED_TAG in tags:
                continue
            if any(tag in EXCLUDED_TAGS for tag in tags):
                continue
            if any(x in name_lower for x in NAME_EXCLUSIONS):
                continue
            group_filtered.append(torrent)

        if len(group_filtered) <= 1:
            continue

        largest = max(group_filtered, key=lambda t: t.total_size)
        for torrent in group_filtered:
            if torrent.hash == largest.hash:
                continue

            reason_text = f"duplicate of {largest.name}"
            if args.dry_run:
                log_and_print(f"⚠️  (DRY RUN) Would delete duplicate: {torrent.name} (Reason: {reason_text})")
            else:
                log_and_print(f"❌ Removing duplicate: {torrent.name} (Reason: {reason_text})")
                qbt.torrents_delete(torrent_hashes=torrent.hash, delete_files=True)
            total_removed += 1

    log_and_print(f"\n✅ Dedupe complete. Removed {total_removed} duplicate movie torrent{'s' if total_removed != 1 else ''}.\n")
# === Mode: Aged or Autobrr ===
if args.mode in ["aged", "autobrr"]:
    total_deleted = 0
    for torrent in torrents:
        tags = [t.strip().lower() for t in torrent.tags.split(",")] if torrent.tags else []
        category = torrent.category.lower() if torrent.category else ""
        name_lower = torrent.name.lower()

        is_stalled = torrent.state.startswith("stalled")
        has_autobrr_category = category == "autobrr"
        has_excluded_tag = any(tag in EXCLUDED_TAGS for tag in tags)
        name_has_exclusion = any(x in name_lower for x in NAME_EXCLUSIONS)

        age_seconds = now - torrent.added_on
        is_old = age_seconds >= AGE_THRESHOLD_SEC
        is_small = torrent.total_size <= SIZE_THRESHOLD_BYTES

        remove_due_to_autobrr = is_stalled and has_autobrr_category
        remove_due_to_age_size = is_old and is_small and not has_excluded_tag and not name_has_exclusion

        log_and_print(f"▶️  Checking: {torrent.name}")
        log_and_print(f"   - Tags: {tags}")
        log_and_print(f"   - Category: {category}")
        log_and_print(f"   - State: {torrent.state}")
        log_and_print(f"   - Size: {torrent.total_size / (1024 ** 3):.2f} GB")
        log_and_print(f"   - Age: {age_seconds // 86400} days")

        should_remove = False
        reasons = []

        if args.mode == "autobrr" and remove_due_to_autobrr:
            reasons.append("stalled & category 'autobrr'")
            should_remove = True

        if args.mode == "aged" and remove_due_to_age_size:
            reasons.append(f"> {DAYS_THRESHOLD} days old & <= {SIZE_THRESHOLD_GB}GB (no excluded tags)")
            should_remove = True

        if should_remove:
            reason_text = " and ".join(reasons)
            if args.dry_run:
                log_and_print(f"⚠️  (DRY RUN) Would delete torrent: {torrent.name} (Reason: {reason_text})\n")
            else:
                log_and_print(f"❌ Removing torrent: {torrent.name} (Reason: {reason_text})\n")
                qbt.torrents_delete(torrent_hashes=torrent.hash, delete_files=True)
                total_deleted += 1
        else:
            log_and_print("✅ Keeping torrent\n")

    if total_deleted == 0 and not args.dry_run:
        log_and_print("✅ No matching torrents to delete. Cleanup complete.\n")
