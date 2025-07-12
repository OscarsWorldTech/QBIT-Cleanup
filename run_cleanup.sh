#!/bin/bash

cd /home/qbitadmin/qbitclean
source .venv/bin/activate

# Accept mode from cron
MODE=$1
LOG="cleanup-${MODE}.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Running $MODE cleanup..." >> "$LOG"
python3 qbit_cleanup.py --mode "$MODE" >> "$LOG" 2>&1
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Finished $MODE cleanup." >> "$LOG"
echo "" >> "$LOG"
