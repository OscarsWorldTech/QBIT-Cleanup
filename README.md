## QBIT Cleanup
<<<<<<< HEAD
=======

A Python script to automatically clean up your qBittorrent instance by:

* Removing **stalled torrents** tagged or categorized with `autobrr` (checked every 5 minutes)
* Deleting **old and small torrents** that are older than a certain number of days and below a certain size (checked daily)

---

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/OscarsWorldTech/QBIT-Cleanup.git
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

### 4. Create Your `.env` File

Copy the example:

```bash
cp .env.example .env
```

Then fill in your qBittorrent credentials:

```ini
QBT_HOST=local
QBT_PORT=8080
QBT_USERNAME=admin
QBT_PASSWORD=yourpassword
```

---

## Usage

### Run Autobrr Cleanup (Every 5 Minutes)

Removes stalled torrents with the `autobrr` category:

```bash
python3 qbit_cleanup.py --mode autobrr
```

### Run Aged Cleanup (Every 24 Hours)

Removes torrents older than X days and smaller than Y GB, skipping those tagged `tv`, `movies`, or containing `ebook`/`nsw` in the name:

```bash
python3 qbit_cleanup.py --mode aged
```

---

## Automation with Cron

You can automate both modes using cron:

```bash
crontab -e
```

Add the following lines:

```cron
# Run autobrr cleanup every 5 minutes
*/5 * * * * /path/to/run_cleanup.sh autobrr

# Run aged cleanup daily at midnight
0 0 * * * /path/to/run_cleanup.sh aged
```

---

## Logging

All output is saved to:

* `cleanup-autobrr.log`
* `cleanup-aged.log`

Log rotation is handled with `logrotate` — see `logrotate.conf` example if provided.

---

Contributions welcome!
# qbit_cleanup
>>>>>>> 1edf09a (Added dedupe logic with dry run capabilities)

A Python script to automatically clean up your qBittorrent instance by:

* Removing **stalled torrents** tagged or categorized with `autobrr` (checked every 5 minutes)
* Deleting **old and small torrents** that are older than a certain number of days and below a certain size (checked daily)

---

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/OscarsWorldTech/QBIT-Cleanup.git
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

### 4. Create Your `.env` File

Copy the example:

```bash
cp .env.example .env
```

Then fill in your qBittorrent credentials:

```ini
QBT_HOST=local
QBT_PORT=8080
QBT_USERNAME=admin
QBT_PASSWORD=yourpassword
```

---

## Usage

### Run Autobrr Cleanup (Every 5 Minutes)

Removes stalled torrents with the `autobrr` category:

```bash
python3 qbit_cleanup.py --mode autobrr
```

### Run Aged Cleanup (Every 24 Hours)

Removes torrents older than X days and smaller than Y GB, skipping those tagged `tv`, `movies`, or containing `ebook`/`nsw` in the name:

```bash
python3 qbit_cleanup.py --mode aged
```

---

## Automation with Cron

You can automate both modes using cron:

```bash
crontab -e
```

Add the following lines:

```cron
# Run autobrr cleanup every 5 minutes
*/5 * * * * /path/to/run_cleanup.sh autobrr

# Run aged cleanup daily at midnight
0 0 * * * /path/to/run_cleanup.sh aged
```

---

## Logging

All output is saved to:

* `cleanup-autobrr.log`
* `cleanup-aged.log`

Log rotation is handled with `logrotate` — see `logrotate.conf` example if provided.

---

Contributions welcome!
