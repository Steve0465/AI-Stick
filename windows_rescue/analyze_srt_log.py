#!/usr/bin/env python3
"""
Windows SRT Log Analyzer
Analyzes System Restore Trial logs from Windows Recovery
"""
import sys
import re
from pathlib import Path

def analyze_srt_log(log_path):
    """Analyze Windows SRT (System Restore Trial) log"""

    print("╔═══════════════════════════════════════════════════════════╗")
    print("║        WINDOWS AUTOMATIC REPAIR LOG ANALYZER             ║")
    print("╚═══════════════════════════════════════════════════════════╝\n")

    try:
        with open(log_path, 'r', encoding='utf-16-le', errors='ignore') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Try different encodings
        try:
            with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except:
            with open(log_path, 'r', encoding='latin-1', errors='ignore') as f:
                content = f.read()

    print("📄 Log file:", log_path)
    print("=" * 70)

    # Extract key information
    errors = []
    warnings = []
    root_causes = []

    for line in content.split('\n'):
        line = line.strip()

        # Look for error patterns
        if 'error' in line.lower() or 'fail' in line.lower():
            errors.append(line)

        if 'warning' in line.lower():
            warnings.append(line)

        # Root cause indicators
        if any(keyword in line.lower() for keyword in [
            'root cause', 'corrupt', 'missing', 'boot', 'bcd',
            'registry', 'disk', 'partition'
        ]):
            root_causes.append(line)

    # Display findings
    if root_causes:
        print("\n🔴 ROOT CAUSES FOUND:")
        for i, cause in enumerate(root_causes[:10], 1):
            print(f"{i}. {cause[:100]}")

    if errors:
        print("\n❌ ERRORS DETECTED:")
        for i, error in enumerate(errors[:10], 1):
            print(f"{i}. {error[:100]}")

    if warnings:
        print("\n⚠️  WARNINGS:")
        for i, warning in enumerate(warnings[:5], 1):
            print(f"{i}. {warning[:100]}")

    print("\n" + "=" * 70)

    # AI-powered diagnosis
    print("\n🤖 DIAGNOSING ISSUE WITH AI...\n")

    # Prepare summary for AI
    summary = f"""Windows Automatic Repair failed. Log analysis:

Root causes found: {len(root_causes)}
Errors found: {len(errors)}
Warnings found: {len(warnings)}

Key indicators:
{chr(10).join(root_causes[:5])}

{chr(10).join(errors[:5])}
"""

    # Check if we can reach Ollama
    try:
        import requests

        response = requests.post('http://localhost:11434/api/generate',
            json={
                "model": "mistral",
                "prompt": f"""{summary}

Based on this Windows SRT log analysis, provide:
1. Most likely root cause
2. Step-by-step fix instructions
3. Data backup recommendations
4. Alternative recovery options

Be specific and actionable.""",
                "stream": False
            },
            timeout=60)

        diagnosis = response.json()['response']
        print(diagnosis)

    except:
        print("⚠️  Cannot reach AI (Ollama not available)")
        print("    Run this script on the Pi for AI-powered diagnosis")

        # Provide basic diagnosis
        print("\n📋 COMMON FIXES:\n")

        if any('bcd' in str(root_causes).lower() or 'boot' in str(root_causes).lower()):
            print("🔧 Boot Configuration Issue Detected:")
            print("   1. Boot from AI_STICK (Ventoy)")
            print("   2. Use Windows PE or Linux live system")
            print("   3. Run: bootrec /fixmbr")
            print("   4. Run: bootrec /fixboot")
            print("   5. Run: bootrec /rebuildbcd\n")

        if any('corrupt' in str(root_causes).lower() or 'registry' in str(root_causes).lower()):
            print("🔧 System File Corruption Detected:")
            print("   1. Boot into Safe Mode (if possible)")
            print("   2. Run: sfc /scannow")
            print("   3. Run: DISM /Online /Cleanup-Image /RestoreHealth")
            print("   4. Or use Windows PE to run these commands\n")

        if any('disk' in str(root_causes).lower()):
            print("🔧 Disk Issue Detected:")
            print("   1. Check disk health with: chkdsk /f /r")
            print("   2. Backup data FIRST if possible")
            print("   3. Consider disk replacement if failing\n")

    # Show full log option
    print("\n" + "=" * 70)
    show_full = input("\n📄 Show full log? (y/n): ").lower()
    if show_full == 'y':
        print("\n" + "=" * 70)
        print(content)
        print("=" * 70)

    # Save analysis
    output_path = log_path.replace('.txt', '_ANALYSIS.txt')
    with open(output_path, 'w') as f:
        f.write(f"Windows SRT Log Analysis\n")
        f.write(f"=" * 70 + "\n\n")
        f.write(f"Root Causes:\n")
        for cause in root_causes:
            f.write(f"  - {cause}\n")
        f.write(f"\nErrors:\n")
        for error in errors[:20]:
            f.write(f"  - {error}\n")

    print(f"\n✅ Analysis saved to: {output_path}")

def scan_for_logs(drive_path):
    """Scan drive for Windows recovery logs"""
    print("🔍 Scanning for Windows recovery logs...\n")

    recovery_paths = [
        "recovery/WindowsRE/winre.wim/system32/logfiles/SRT",
        "Windows/System32/LogFiles/SRT",
        "recovery/logs",
    ]

    found_logs = []

    for recovery_path in recovery_paths:
        full_path = Path(drive_path) / recovery_path
        if full_path.exists():
            for log_file in full_path.glob('*.txt'):
                found_logs.append(log_file)
                print(f"   ✅ Found: {log_file}")

    return found_logs

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Windows SRT Log Analyzer\n")
        print("Usage:")
        print("  ./analyze_srt_log.py /path/to/SRTtrial.txt")
        print("  ./analyze_srt_log.py /mnt/windows  # Scan entire drive")
        print("\nExample:")
        print("  ./analyze_srt_log.py /mnt/windows/recovery/WindowsRE/winre.wim/system32/logfiles/SRT/SRTtrial.txt")
        sys.exit(1)

    path = sys.argv[1]

    if Path(path).is_file():
        analyze_srt_log(path)
    elif Path(path).is_dir():
        logs = scan_for_logs(path)
        if logs:
            print(f"\nFound {len(logs)} log file(s)")
            print("\nAnalyze which one?")
            for i, log in enumerate(logs, 1):
                print(f"{i}. {log}")

            choice = input("\nEnter number (or 'all'): ").strip()

            if choice.lower() == 'all':
                for log in logs:
                    analyze_srt_log(str(log))
                    print("\n" + "=" * 70 + "\n")
            else:
                try:
                    idx = int(choice) - 1
                    analyze_srt_log(str(logs[idx]))
                except:
                    print("Invalid choice")
        else:
            print("❌ No Windows recovery logs found")
    else:
        print(f"❌ Path not found: {path}")
