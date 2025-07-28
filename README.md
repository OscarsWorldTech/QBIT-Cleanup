QBIT Cleanup
A Python script to automatically clean up your qBittorrent instance by:

🚫 Removing stalled torrents tagged or categorized with autobrr (every 5 minutes)

🧹 Deleting old and small torrents older than a set number of days and smaller than a size threshold (daily)

🔁 Deduplicating movie torrents, keeping the largest or cross-seeded ones

🔧 Setup
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/OscarsWorldTech/QBIT-Cleanup.git
cd QBIT-Cleanup
2. Create and Activate a Virtual Environment
bash
Copy
Edit
python3 -m venv .venv
source .venv/bin/activate
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Create Your .env File
bash
Copy
Edit
cp .env.example .env
Then fill in your qBittorrent credentials:

env
Copy
Edit
QBT_HOST=local
QBT_PORT=8080
QBT_USERNAME=admin
QBT_PASSWORD=yourpassword
🚀 Usage
Run Autobrr Cleanup (every 5 minutes)
Removes stalled torrents with the autobrr category or tag:

bash
Copy
Edit
python3 qbit_cleanup.py --mode autobrr
Run Aged Cleanup (every 24 hours)
Removes torrents that are:

older than X days

smaller than Y GB
(excludes torrents tagged with movies, tv, or filenames containing ebook or nsw)

bash
Copy
Edit
python3 qbit_cleanup.py --mode aged
Run Deduplication (optional, e.g. weekly)
Keeps only the largest movie torrent, or one with a cross-seed tag:

bash
Copy
Edit
python3 qbit_cleanup.py --mode dedupe
To simulate without deleting anything:

bash
Copy
Edit
python3 qbit_cleanup.py --mode dedupe --dry-run
⏱ Automation with Cron
bash
Copy
Edit
crontab -e
Example entries:

cron
Copy
Edit
# Run autobrr cleanup every 5 minutes
*/5 * * * * /path/to/run_cleanup.sh autobrr

# Run aged cleanup daily at midnight
0 0 * * * /path/to/run_cleanup.sh aged

# Optional: Run dedupe every Sunday at 3am
0 3 * * 0 /path/to/run_cleanup.sh dedupe
📜 Logging
Logs are written to:

cleanup-autobrr.log

cleanup-aged.log

cleanup---autobrr.log, etc. (with rotation)

Log rotation is handled via logrotate. Check logrotate.conf if provided.

🤝 Contributions Welcome
PRs, issues, and feedback are encouraged!
