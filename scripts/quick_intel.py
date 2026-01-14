#!/usr/bin/env python3
"""
Quick Intel - Gather useful info from any system this stick touches

ETHICAL USE ONLY - For your own systems or with permission
"""

import os
import sys
import json
import socket
import platform
import subprocess
from pathlib import Path
from datetime import datetime

STICK = Path("/Volumes/AI_STICK") if sys.platform == "darwin" else Path("/media/AI_STICK")
OUTPUT = STICK / "results/intel"


def get_system_info():
    """Basic system information."""
    return {
        "hostname": socket.gethostname(),
        "platform": platform.platform(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "python": platform.python_version(),
        "user": os.environ.get("USER", os.environ.get("USERNAME", "unknown")),
        "home": str(Path.home()),
    }


def get_network_info():
    """Network configuration."""
    info = {"interfaces": [], "wifi_networks": []}
    
    try:
        if sys.platform == "darwin":
            # macOS
            result = subprocess.run(["ifconfig"], capture_output=True, text=True)
            info["ifconfig"] = result.stdout[:2000]  # Truncate
            
            # WiFi networks (requires airport utility)
            try:
                result = subprocess.run(
                    ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-s"],
                    capture_output=True, text=True, timeout=10
                )
                info["wifi_scan"] = result.stdout[:1000]
            except:
                pass
        else:
            # Linux
            result = subprocess.run(["ip", "addr"], capture_output=True, text=True)
            info["ip_addr"] = result.stdout[:2000]
    except:
        pass
    
    return info


def get_installed_apps():
    """List of installed applications."""
    apps = []
    
    if sys.platform == "darwin":
        app_dirs = [Path("/Applications"), Path.home() / "Applications"]
        for app_dir in app_dirs:
            if app_dir.exists():
                apps.extend([a.name for a in app_dir.glob("*.app")])
    
    return sorted(set(apps))[:50]  # Top 50


def get_browser_bookmarks():
    """Find browser bookmark files (paths only, not content)."""
    bookmarks = {}
    home = Path.home()
    
    paths = {
        "chrome": home / "Library/Application Support/Google/Chrome/Default/Bookmarks",
        "firefox": home / "Library/Application Support/Firefox/Profiles",
        "safari": home / "Library/Safari/Bookmarks.plist",
        "brave": home / "Library/Application Support/BraveSoftware/Brave-Browser/Default/Bookmarks",
    }
    
    for browser, path in paths.items():
        bookmarks[browser] = str(path) if path.exists() else None
    
    return bookmarks


def get_ssh_keys():
    """Check for SSH key presence (not content)."""
    ssh_dir = Path.home() / ".ssh"
    if not ssh_dir.exists():
        return {"exists": False}
    
    keys = [f.name for f in ssh_dir.iterdir() if f.is_file()]
    return {
        "exists": True,
        "files": keys,
        "has_private_keys": any(not k.endswith(".pub") and k.startswith("id_") for k in keys),
    }


def get_cloud_configs():
    """Check for cloud service configurations."""
    home = Path.home()
    services = {
        "aws": home / ".aws/credentials",
        "gcloud": home / ".config/gcloud",
        "azure": home / ".azure",
        "docker": home / ".docker/config.json",
        "kube": home / ".kube/config",
    }
    
    return {name: path.exists() for name, path in services.items()}


def main():
    print("=" * 50)
    print("🔍 QUICK INTEL GATHER")
    print("=" * 50)
    
    OUTPUT.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    hostname = socket.gethostname().replace(" ", "_")
    
    report = {
        "timestamp": timestamp,
        "system": get_system_info(),
        "network": get_network_info(),
        "apps": get_installed_apps(),
        "browsers": get_browser_bookmarks(),
        "ssh": get_ssh_keys(),
        "cloud": get_cloud_configs(),
    }
    
    # Save report
    report_path = OUTPUT / f"intel_{hostname}_{timestamp}.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n📊 System: {report['system']['platform']}")
    print(f"👤 User: {report['system']['user']}")
    print(f"📱 Apps: {len(report['apps'])} found")
    print(f"🔑 SSH keys: {'Yes' if report['ssh'].get('has_private_keys') else 'No'}")
    print(f"☁️ Cloud configs: {[k for k,v in report['cloud'].items() if v]}")
    print(f"\n✅ Report saved: {report_path.name}")


if __name__ == "__main__":
    main()
