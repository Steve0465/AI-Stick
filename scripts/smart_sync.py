#!/usr/bin/env python3
"""
Smart Sync - Intelligent sync between Mac, Pi, and AI_STICK

Detects current environment and syncs appropriately:
- On Mac: Sync to stick, push to Pi if available
- On Pi: Pull from stick, update knowledge, backup to stick
- Auto-detects Tailscale connections
"""

import os
import sys
import json
import subprocess
import socket
from pathlib import Path
from datetime import datetime
import shutil

# Detect environment
IS_MAC = sys.platform == "darwin"
IS_LINUX = sys.platform == "linux"
IS_PI = IS_LINUX and Path("/proc/device-tree/model").exists()

# Paths
if IS_MAC:
    STICK = Path("/Volumes/AI_STICK")
    HOME = Path.home()
elif IS_PI:
    STICK = Path("/media/ai_stick")
    HOME = Path.home()
else:
    STICK = Path("/media/AI_STICK")
    HOME = Path.home()


def run(cmd):
    """Run command and return output."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=30
        )
        return result.stdout.strip()
    except:
        return ""


def get_tailscale_devices():
    """Get list of Tailscale devices on network."""
    devices = []
    status = run("tailscale status --json 2>/dev/null")
    if status:
        try:
            data = json.loads(status)
            for peer in data.get('Peer', {}).values():
                devices.append({
                    'hostname': peer.get('HostName'),
                    'ip': peer.get('TailscaleIPs', [''])[0],
                    'online': peer.get('Online', False)
                })
        except:
            pass
    return devices


def sync_to_stick_mac():
    """Sync from Mac to stick."""
    print("📦 MAC → STICK SYNC")
    print("=" * 50)

    if not STICK.exists():
        print("❌ AI_STICK not mounted")
        return

    # Sync Documents
    docs_dest = STICK / "Exports" / "Mac_Documents"
    docs_dest.mkdir(parents=True, exist_ok=True)

    print("\n📄 Syncing recent documents...")
    docs = HOME / "Documents"
    if docs.exists():
        # Only sync recent files (last 7 days)
        count = 0
        for ext in ['.pdf', '.docx', '.txt', '.md']:
            for f in docs.rglob(f"*{ext}"):
                if f.is_file() and not f.name.startswith('.'):
                    age_days = (datetime.now().timestamp() - f.stat().st_mtime) / 86400
                    if age_days <= 7:
                        dest = docs_dest / f.name
                        if not dest.exists() or f.stat().st_mtime > dest.stat().st_mtime:
                            shutil.copy2(f, dest)
                            count += 1
        print(f"   ✅ Synced {count} recent documents")

    # Backup SSH keys (safely)
    ssh_backup = STICK / "Exports" / "ssh_backup"
    ssh_backup.mkdir(parents=True, exist_ok=True)

    ssh_dir = HOME / ".ssh"
    if ssh_dir.exists():
        print("\n🔑 Backing up SSH config...")
        for f in ['config', 'known_hosts']:
            src = ssh_dir / f
            if src.exists():
                shutil.copy2(src, ssh_backup / f)
        print("   ✅ SSH config backed up (keys NOT copied for security)")

    # Sync Downloads recent
    downloads_dest = STICK / "_transfer_zone" / "Mac_Downloads"
    downloads_dest.mkdir(parents=True, exist_ok=True)

    downloads = HOME / "Downloads"
    if downloads.exists():
        print("\n📥 Syncing recent downloads...")
        count = 0
        for f in downloads.iterdir():
            if f.is_file() and not f.name.startswith('.'):
                age_days = (datetime.now().timestamp() - f.stat().st_mtime) / 86400
                if age_days <= 3:  # Last 3 days
                    dest = downloads_dest / f.name
                    if not dest.exists():
                        shutil.copy2(f, dest)
                        count += 1
        print(f"   ✅ Synced {count} recent downloads")

    print("\n✅ Mac → Stick sync complete")


def sync_from_stick_pi():
    """Sync from stick to Pi."""
    print("📦 STICK → PI SYNC")
    print("=" * 50)

    if not STICK.exists():
        print("❌ AI_STICK not mounted")
        return

    # Pull new scripts
    print("\n📜 Updating scripts...")
    pi_scripts = HOME / "ai_scripts"
    pi_scripts.mkdir(exist_ok=True)

    stick_scripts = STICK / "scripts"
    if stick_scripts.exists():
        count = 0
        for f in stick_scripts.glob("*.py"):
            dest = pi_scripts / f.name
            if not dest.exists() or f.stat().st_mtime > dest.stat().st_mtime:
                shutil.copy2(f, dest)
                os.chmod(dest, 0o755)
                count += 1
        print(f"   ✅ Updated {count} scripts")

    # Process transfers
    transfer_zone = STICK / "_transfer_zone"
    if transfer_zone.exists():
        print("\n📥 Processing transfers...")
        for item in transfer_zone.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                print(f"   Found: {item.name}")

    print("\n✅ Stick → Pi sync complete")


def backup_to_stick_pi():
    """Backup Pi state to stick."""
    print("💾 PI → STICK BACKUP")
    print("=" * 50)

    if not STICK.exists():
        print("❌ AI_STICK not mounted")
        return

    backup_dir = STICK / "Exports" / "pi_backups"
    backup_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Backup crontabs
    print("\n⏰ Backing up crontab...")
    crontab = run("crontab -l 2>/dev/null")
    if crontab:
        (backup_dir / f"crontab_{timestamp}.txt").write_text(crontab)
        print("   ✅ Crontab backed up")

    # Backup systemd services
    print("\n🔧 Backing up custom services...")
    services_dir = backup_dir / "systemd_services"
    services_dir.mkdir(exist_ok=True)

    for service in ['ollama', 'kiwix']:
        service_file = Path(f"/etc/systemd/system/{service}.service")
        if service_file.exists():
            shutil.copy2(service_file, services_dir / service_file.name)
    print("   ✅ Services backed up")

    # List installed Ollama models
    print("\n🤖 Recording Ollama models...")
    models = run("ollama list 2>/dev/null")
    if models:
        (backup_dir / f"ollama_models_{timestamp}.txt").write_text(models)
        print("   ✅ Model list saved")

    print("\n✅ Pi → Stick backup complete")


def check_pi_connection():
    """Check if Pi is available on Tailscale."""
    devices = get_tailscale_devices()
    for d in devices:
        if d['online'] and ('pi' in d['hostname'].lower() or 'aiserver' in d['hostname'].lower()):
            return d
    return None


def sync_mac_to_pi():
    """Sync from Mac to Pi via Tailscale."""
    print("\n🔄 Checking for Pi connection...")

    pi = check_pi_connection()
    if not pi:
        print("   ⚠️  Pi not found on Tailscale network")
        return

    print(f"   ✅ Found Pi: {pi['hostname']} ({pi['ip']})")

    # TODO: rsync implementation
    print("   📡 Direct Mac → Pi sync (coming soon)")


def main():
    print("╔════════════════════════════════════════════════════════╗")
    print("║              🔄 SMART SYNC                             ║")
    print("╚════════════════════════════════════════════════════════╝")
    print("")

    hostname = socket.gethostname()
    print(f"🖥️  Device: {hostname}")
    print(f"📍 Platform: {'Mac' if IS_MAC else 'Pi' if IS_PI else 'Linux'}")
    print(f"💾 Stick: {'✅ Mounted' if STICK.exists() else '❌ Not found'}")
    print("")

    if not STICK.exists():
        print("❌ AI_STICK not found. Please mount it first.")
        sys.exit(1)

    # Check Tailscale
    ts_ip = run("tailscale ip -4 2>/dev/null")
    if ts_ip:
        print(f"🔗 Tailscale: {ts_ip}")
    print("")

    if IS_MAC:
        # Mac operations
        print("📋 SYNC OPTIONS:")
        print("1. Sync Mac → Stick (backup recent files)")
        print("2. Check Pi status")
        print("3. Sync Mac → Pi (via Tailscale)")
        print("")

        choice = input("Select option (1-3): ").strip()

        if choice == '1':
            sync_to_stick_mac()
        elif choice == '2':
            devices = get_tailscale_devices()
            if devices:
                print("\n🌐 Tailscale Devices:")
                for d in devices:
                    status = "🟢" if d['online'] else "🔴"
                    print(f"   {status} {d['hostname']} - {d['ip']}")
            else:
                print("No devices found")
        elif choice == '3':
            sync_mac_to_pi()

    elif IS_PI:
        # Pi operations
        print("📋 SYNC OPTIONS:")
        print("1. Pull updates from Stick")
        print("2. Backup Pi state to Stick")
        print("3. Full sync (both directions)")
        print("")

        choice = input("Select option (1-3): ").strip()

        if choice == '1':
            sync_from_stick_pi()
        elif choice == '2':
            backup_to_stick_pi()
        elif choice == '3':
            sync_from_stick_pi()
            backup_to_stick_pi()

    print("")
    print("✅ Sync operations complete!")


if __name__ == "__main__":
    main()
