# fsociety_tools (macOS)

This folder contains a curated set of common security tools often referenced by fsociety. Each tool sits in its own subfolder with a README describing what it does and quick usage.

## Contents
- nmap — Network scanner
- sqlmap — SQL injection automation (Python)
- wpscan — WordPress scanner (Ruby)
- XSStrike — XSS scanner (Python)
- commix — Command injection tool (Python)
- reaver-wps-fork-t6x — WPS brute force (native build)
- pixiewps — Pixie Dust attack (native build)
- social-engineer-toolkit — Phishing & social engineering (Python)
- ncrack — Network auth cracker
- cupp — Wordlist generator (Python)

## Install Dependencies (macOS)
You can copy/paste the commands below to install runtime dependencies.

### 0) Ruby PATH (recommended)
Add Homebrew Ruby to your PATH so `wpscan` and gems are available:
export PATH="/opt/homebrew/opt/ruby/bin:$PATH"

### 1) Homebrew (if missing)
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" || true

### 2) Core packages
brew update
brew install python3 nmap ncrack ruby git openssl libffi

### 3) Python tools
python3 -m pip install --upgrade pip
# sqlmap, XSStrike, commix, cupp (run directly from cloned repos)

### 4) Social-Engineer Toolkit deps
cd social-engineer-toolkit
python3 -m pip install -r requirements.txt
cd ..

### 5) Ruby tools (wpscan)
# Ensure Ruby and Bundler are ready
gem install bundler -v 2.4.22
gem install public_suffix -v 5.1.1
gem install wpscan
# Update DB (optional)
wpscan --update

### 6) Build native tools
# Reaver
cd reaver-wps-fork-t6x
./configure || true
make
sudo make install || true
cd ..
# Pixiewps
cd pixiewps
make
sudo make install || true
cd ..

## Running Examples
- nmap: nmap -sV scanme.nmap.org
- sqlmap: cd sqlmap && python3 sqlmap.py -u "https://target/?id=1" --batch
- wpscan: wpscan --url https://example.com
- XSStrike: cd XSStrike && python3 xsstrike.py -u https://example.com
- commix: cd commix && python3 commix.py --url=https://example.com/?id=1
- reaver: sudo reaver -i en0 -b DE:AD:BE:EF:00:01
- pixiewps: sudo pixiewps -e <pke> -s <pkr> -z <hash>
- SET: cd social-engineer-toolkit && python3 setoolkit
- ncrack: ncrack -p 22,80 192.0.2.10
- cupp: cd cupp && python3 cupp.py -i

## Notes
- Use these tools only on systems you have explicit authorization to test.
- Some tools require additional drivers or privileges (e.g., Wi‑Fi chipsets for reaver).
- On macOS, `sudo` may prompt for your password when installing or running some commands.
 - If `wpscan` is not found, ensure Ruby PATH is exported (step 0).
