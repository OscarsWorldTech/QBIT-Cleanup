#!/usr/bin/env python3

"""
qBittorrent Cleanup Script with Modes
Usage:
  python3 qbit_cleanup.py --mode autobrr   # every 5 min
  python3 qbit_cleanup.py --mode aged      # every 24 hrs
"""
import os
import time
import argparse
from qbittorrentapi import Client, LoginFailed
from dotenv import load_dotenv

load_dotenv()


# === Parse CLI arguments ===
parser = argparse.ArgumentParser(description="qBittorrent Cleanup Script")
parser.add_argument(
    "--mode",
    choices=["autobrr", "aged"],
    required=True,
    help="Cleanup mode: 'autobrr' for stalled downloads, 'aged' for old small torrents",
)
args = parser.parse_args()

# === Configuration ===
QBT_HOST = os.getenv("QBT_HOST")
QBT_PORT = int(os.getenv("QBT_PORT"))
QBT_USERNAME = os.getenv("QBT_USERNAME")
QBT_PASSWORD = os.getenv("QBT_PASSWORD")  # <-- replace with your real password

DAYS_THRESHOLD = 15
SIZE_THRESHOLD_GB = 5
AGE_THRESHOLD_SEC = DAYS_THRESHOLD * 24 * 3600
SIZE_THRESHOLD_BYTES = SIZE_THRESHOLD_GB * 1024**3

EXCLUDED_TAGS = {"movies", "tv"}
NAME_EXCLUSIONS = ["nsw", "ebook"]

# === Connect to qBittorrent ===
qbt = Client(
    host=QBT_HOST,
    port=QBT_PORT,
    username=QBT_USERNAME,
    password=QBT_PASSWORD,
)

try:
    qbt.auth_log_in()
except LoginFailed as e:
    print(f"ERROR: Login failed - {e}")
    exit(1)

torrents = qbt.torrents_info()
now = int(time.time())

print(f"\n📦 Total torrents found: {len(torrents)}")
print(f"🚀 Running in mode: {args.mode}\n")


while True:
    torrents = qbt.torrents_info()
    now = int(time.time())

    total_deleted = 0

    for torrent in torrents:
        tags = [t.strip().lower() for t in torrent.tags.split(",")] if torrent.tags else []
        category = torrent.category.lower() if torrent.category else ""

        is_stalled = torrent.state.startswith("stalled")
        has_autobrr_category = category == "autobrr"
        has_excluded_tag = any(tag in EXCLUDED_TAGS for tag in tags)
        name_has_exclusion = any(x in torrent.name.lower() for x in NAME_EXCLUSIONS)
        is_incomplete = not torrent.progress == 1.0


        age_seconds = now - torrent.added_on
        is_old = age_seconds >= AGE_THRESHOLD_SEC
        is_small = torrent.total_size <= SIZE_THRESHOLD_BYTES

        remove_due_to_autobrr = is_stalled and has_autobrr_category and is_incomplete
        remove_due_to_age_size = is_old and is_small and not has_excluded_tag and not name_has_exclusion

        print(f"▶️  Checking: {torrent.name}")
        print(f"   - Tags: {tags}")
        print(f"   - Category: {category}")
        print(f"   - State: {torrent.state}")
        print(f"   - Size: {torrent.total_size / (1024 ** 3):.2f} GB")
        print(f"   - Age: {age_seconds // 86400} days")

        if args.mode == "aged" and name_has_exclusion:
            print(f"⚠️ Skipping (excluded by name match): {torrent.name}\n")

        should_remove = False
        reasons = []

        if args.mode == "autobrr" and remove_due_to_autobrr:
            reasons.append("stalled & categorized 'autobrr'")
            should_remove = True

        if args.mode == "aged" and remove_due_to_age_size:
            reasons.append(f"> {DAYS_THRESHOLD} days old & <= {SIZE_THRESHOLD_GB}GB (no excluded tag or keyword)")
            should_remove = True

        if should_remove:
            reason_text = " and ".join(reasons)
            print(f"❌ Removing torrent: \"{torrent.name}\" (Reason: {reason_text})\n")
            qbt.torrents_delete(torrent_hashes=torrent.hash, delete_files=True)
            total_deleted += 1
        else:
            print("✅ Keeping torrent\n")

    # Exit loop if no more matching torrents
    if total_deleted == 0:
        print("✅ No more matching torrents to delete. Cleanup complete.\n")
        break
    else:
        print(f"🔁 Deleted {total_deleted} torrents, checking again...\n")
        time.sleep(10)
