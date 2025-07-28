## 📦 QBIT Cleanup

A Python script to automatically clean up your qBittorrent instance by:

- 🚫 Removing stalled torrents tagged or categorized with `autobrr` (every 5 minutes)
- 🧹 Deleting old and small torrents older than a set number of days and smaller than a size threshold (daily)
- 🔁 Deduplicating movie torrents, keeping only the largest or one with a cross-seed tag (optional)

---

## 📁 Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/QBIT-Cleanup.git
cd QBIT-Cleanup
```

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn’t exist:

```bash
pip install qbittorrent-api python-dotenv
```

### 4. Create Your `.env` File

Copy the example:

```bash
cp .env.example .env
```

Then update it with your qBittorrent details:

```ini
QBT_HOST=localhost
QBT_PORT=8080
QBT_USERNAME=admin
QBT_PASSWORD=yourpassword
```

---

## 🚀 Usage

### Run Autobrr Cleanup (Every 5 Minutes)

Removes stalled torrents tagged or categorized as autobrr.

```bash
python3 qbit_cleanup.py --mode autobrr
```

### Run Aged Cleanup (Every 24 Hours)

Removes torrents older than a threshold and smaller than a size (excluding those tagged `tv`, `movies`, or with `ebook` or `nsw` in the name).

```bash
python3 qbit_cleanup.py --mode aged
```

### Run Deduplication (e.g. Weekly)

Keeps only the largest torrent for each movie, unless another has a cross-seed tag.

```bash
python3 qbit_cleanup.py --mode dedupe
```

Dry-run example:

```bash
python3 qbit_cleanup.py --mode dedupe --dry-run
```

---

## 🔁 Automation with Cron

Open crontab:

```bash
crontab -e
```

Add entries:

```cron
# Autobrr cleanup every 5 minutes
*/5 * * * * /path/to/run_cleanup.sh autobrr

# Aged cleanup every night at midnight
0 0 * * * /path/to/run_cleanup.sh aged

# Dedupe every Sunday at 3AM (optional)
0 3 * * 0 /path/to/run_cleanup.sh dedupe
```

---

## 📈 Logging

Logs are saved to:

- `cleanup-autobrr.log`
- `cleanup-aged.log`
- `cleanup-dedupe.log`

Supports rotation via `logrotate`. See `logrotate.conf` if included.

---

## 💪 Dry Run Mode

Dry run lets you simulate deletions before committing to changes.

```bash
python3 qbit_cleanup.py --mode aged --dry-run
python3 qbit_cleanup.py --mode dedupe --dry-run
```

---

## 🤝 Contributions Welcome

Pull requests, issues, and feedback are encouraged!
