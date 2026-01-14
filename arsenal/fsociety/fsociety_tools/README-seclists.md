# SecLists (Sparse Checkout)

This guide shows how to fetch only common subsets of SecLists to save space, and provides quick paths you can use with tools.

## Fetch
Run the helper script:

```bash
bash ~/Desktop/fsociety_tools/scripts/seclists-sparse.sh
```

It pulls:
- Discovery/Web-Content
- Discovery/DNS
- Passwords/Leaked-Databases

## Common Paths
- Web content: SecLists/Discovery/Web-Content/common.txt
- DNS names: SecLists/Discovery/DNS/namelist.txt
- RockYou: SecLists/Passwords/Leaked-Databases/rockyou.txt.tar.gz

## Examples
- Gobuster (directories):
```bash
gobuster dir -u https://example.com -w ~/Desktop/fsociety_tools/SecLists/Discovery/Web-Content/common.txt
```
- Wfuzz (parameters):
```bash
wfuzz -c -z file,~/Desktop/fsociety_tools/SecLists/Discovery/Web-Content/common.txt -u "https://example.com/page?user=FUZZ"
```
- DNS brute force:
```bash
gobuster dns -d example.com -w ~/Desktop/fsociety_tools/SecLists/Discovery/DNS/namelist.txt
```

Notes:
- Always use on authorized targets.
- Wordlists are large; sparse checkout keeps disk usage reasonable.
