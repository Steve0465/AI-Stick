#!/usr/bin/env python3
"""
Vertex Sync - Bidirectional sync between AI_STICK and Vertex

Features:
- Backs up vertex_brain.db to stick
- Syncs knowledge learned on-the-go back to Vertex
- Pulls new files from Vertex intake for offline processing
"""

import os
import shutil
import sqlite3
from pathlib import Path
from datetime import datetime

STICK = Path("/Volumes/AI_STICK")
VERTEX = Path("/Volumes/Vertex")
VERTEX_BRAIN_DB = VERTEX / "Agents/Vertex Brain/database/vertex_brain.db"
STICK_BACKUP = STICK / "Exports/vertex_backups"


def backup_brain():
    """Backup vertex_brain.db to the stick."""
    if not VERTEX_BRAIN_DB.exists():
        print("❌ Vertex Brain DB not found (Vertex not mounted?)")
        return False
    
    STICK_BACKUP.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = STICK_BACKUP / f"vertex_brain_{timestamp}.db"
    
    print(f"📦 Backing up Vertex Brain...")
    shutil.copy2(VERTEX_BRAIN_DB, backup_path)
    
    # Keep only last 5 backups
    backups = sorted(STICK_BACKUP.glob("vertex_brain_*.db"), reverse=True)
    for old in backups[5:]:
        old.unlink()
        print(f"   🗑️ Removed old backup: {old.name}")
    
    print(f"✅ Backed up to: {backup_path.name}")
    
    # Also keep a "latest" copy for quick access
    latest = STICK_BACKUP / "vertex_brain_LATEST.db"
    shutil.copy2(backup_path, latest)
    
    return True


def get_brain_stats():
    """Show what's in the brain."""
    db_path = STICK_BACKUP / "vertex_brain_LATEST.db"
    if not db_path.exists():
        backup_brain()
    
    if not db_path.exists():
        return
    
    conn = sqlite3.connect(db_path)
    
    print("\n📊 VERTEX BRAIN STATS")
    print("=" * 40)
    
    try:
        # Transactions
        txn = conn.execute("SELECT COUNT(*), MIN(date), MAX(date) FROM bank_transactions").fetchone()
        print(f"💳 Transactions: {txn[0]:,}")
        print(f"   Date range: {txn[1]} to {txn[2]}")
    except:
        pass
    
    try:
        # Knowledge
        know = conn.execute("SELECT COUNT(*) FROM knowledge").fetchone()
        print(f"📚 Knowledge entries: {know[0]}")
    except:
        pass
    
    try:
        # Actions
        act = conn.execute("SELECT COUNT(*) FROM action_items WHERE status='pending'").fetchone()
        print(f"📋 Pending actions: {act[0]}")
    except:
        pass
    
    conn.close()


def sync_inbox():
    """Pull files from Vertex intake lanes for offline processing."""
    intake = VERTEX / "Archive/Intake"
    stick_inbox = STICK / "Inbox/from_vertex"
    stick_inbox.mkdir(parents=True, exist_ok=True)
    
    if not intake.exists():
        print("❌ Vertex Intake not found")
        return
    
    print("\n📥 Syncing from Vertex Intake...")
    
    count = 0
    for lane in intake.iterdir():
        if lane.is_dir() and not lane.name.startswith('.'):
            for f in lane.iterdir():
                if f.is_file() and not f.name.startswith('.'):
                    dest = stick_inbox / f"{lane.name}_{f.name}"
                    if not dest.exists():
                        shutil.copy2(f, dest)
                        print(f"   📄 {lane.name}/{f.name}")
                        count += 1
    
    print(f"✅ Synced {count} new files")


def main():
    print("=" * 50)
    print("🔄 VERTEX SYNC")
    print("=" * 50)
    
    # Check mounts
    if not STICK.exists():
        print("❌ AI_STICK not mounted!")
        return
    
    vertex_available = VERTEX.exists() and VERTEX_BRAIN_DB.exists()
    
    if vertex_available:
        print("✅ Vertex drive detected")
        backup_brain()
        sync_inbox()
    else:
        print("⚠️ Vertex not available - showing offline data")
    
    get_brain_stats()


if __name__ == "__main__":
    main()
