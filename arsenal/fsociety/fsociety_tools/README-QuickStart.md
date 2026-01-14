# Quick Start

Use this as a reference for the most common commands.

## Environment
```bash
source ~/Desktop/fsociety_tools/env.sh
```

## Update
```bash
bash ~/Desktop/fsociety_tools/update.sh
```

## Smoke Test
```bash
bash ~/Desktop/fsociety_tools/scripts/run-smoke.sh
```

## SecLists (Sparse Subsets)
```bash
cd ~
bash ~/Desktop/fsociety_tools/scripts/seclists-sparse.sh
```
Common paths:
- Web content: ~/Desktop/fsociety_tools/SecLists/Discovery/Web-Content/common.txt
- DNS names:  ~/Desktop/fsociety_tools/SecLists/Discovery/DNS/namelist.txt
- RockYou:    ~/Desktop/fsociety_tools/SecLists/Passwords/Leaked-Databases/rockyou.txt.tar.gz
 
## Small Wordlists (Fast)
Use lightweight curated lists when you want quick scans without cloning full SecLists:
- Web paths: ~/Desktop/fsociety_tools/wordlists-small/web-common.txt
- DNS names: ~/Desktop/fsociety_tools/wordlists-small/dns-small.txt
- Usernames: ~/Desktop/fsociety_tools/wordlists-small/users-small.txt
- Passwords: ~/Desktop/fsociety_tools/wordlists-small/passwords-small.txt

## One-Off Runs
```bash
# Gobuster (dir)
bash ~/Desktop/fsociety_tools/scripts/run-example.sh gobuster https://example.com
 
# Gobuster (dir, small list)
bash ~/Desktop/fsociety_tools/scripts/run-example.sh gobuster https://example.com --wordlist ~/Desktop/fsociety_tools/wordlists-small/web-common.txt

# Gobuster (dns)
bash ~/Desktop/fsociety_tools/scripts/run-example.sh gobuster example.com --mode dns --wordlist ~/Desktop/fsociety_tools/SecLists/Discovery/DNS/namelist.txt
 
# Gobuster (dns, small list)
bash ~/Desktop/fsociety_tools/scripts/run-example.sh gobuster example.com --mode dns --wordlist ~/Desktop/fsociety_tools/wordlists-small/dns-small.txt

# WPScan (token optional)
bash ~/Desktop/fsociety_tools/scripts/run-example.sh wpscan https://example.com --api-token YOUR_TOKEN

# SQLMap
bash ~/Desktop/fsociety_tools/scripts/run-example.sh sqlmap "https://example.com/item.php?id=1" --flags "--batch --risk=1 --level=2"

# Nikto
bash ~/Desktop/fsociety_tools/scripts/run-example.sh nikto https://example.com

# Wfuzz
bash ~/Desktop/fsociety_tools/scripts/run-example.sh wfuzz "https://example.com/page?user=FUZZ" --wordlist ~/Desktop/fsociety_tools/SecLists/Discovery/Web-Content/common.txt

# Wfuzz (small list)
bash ~/Desktop/fsociety_tools/scripts/run-example.sh wfuzz "https://example.com/page?user=FUZZ" --wordlist ~/Desktop/fsociety_tools/wordlists-small/web-common.txt
```

## Fast Defaults
When you want automatic small wordlists without specifying `--wordlist`:
```bash
bash ~/Desktop/fsociety_tools/scripts/run-fast.sh gobuster https://example.com --mode dir
bash ~/Desktop/fsociety_tools/scripts/run-fast.sh gobuster example.com --mode dns
bash ~/Desktop/fsociety_tools/scripts/run-fast.sh wfuzz "https://example.com/page?user=FUZZ"
```

## Multi-Target File
```bash
echo "https://example.com" > /tmp/targets.txt
echo "https://example.org" >> /tmp/targets.txt
bash ~/Desktop/fsociety_tools/scripts/run-example.sh gobuster _ --target-file /tmp/targets.txt --mode dir
```

## Batch Plan
```bash
brew install jq
bash ~/Desktop/fsociety_tools/scripts/run-batch.sh ~/Desktop/fsociety_tools/plan.json
```

## Outputs
- Saved to ~/Desktop/fsociety_tools/output with timestamped filenames.
