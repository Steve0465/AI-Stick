# 🔌 AI STICK - Setup Instructions

## Making the Stick Bootable

Since Ventoy only runs on Linux, here are your options:

### Option A: One-Time Linux Boot (Recommended)
1. Download a small Linux ISO (like Ubuntu Mini or Puppy Linux)
2. Use **balenaEtcher** on Mac to flash it to a DIFFERENT USB
3. Boot from that USB
4. Run Ventoy from there to set up AI_STICK
5. After setup, AI_STICK becomes your multi-boot stick

### Option B: Direct Flash with balenaEtcher
1. Download balenaEtcher: https://etcher.balena.io
2. **BACKUP everything on AI_STICK first!**
3. Flash kali-live.iso directly to the stick
4. You lose multi-boot but get working Kali

### Option C: Use a Linux VM
1. Install VirtualBox or UTM on Mac
2. Boot a Linux ISO in VM
3. Pass through the USB stick to the VM
4. Run Ventoy installer from VM

---

## After Booting Kali

1. Mount AI_STICK: `sudo mount /dev/sda1 /mnt`
2. Install Ollama: `curl -fsSL https://ollama.com/install.sh | sh`
3. Download models: `cd /mnt/models && ./download_models.sh`

## Default Credentials
- Kali: `kali` / `kali`
- n8n: `admin` / `aistick`

## Contents
- 📁 wordlists/ - SecLists, RockYou, DefaultCreds
- 📁 exploits/ - Nuclei, PayloadsAllTheThings, HackTricks
- 📁 osint/ - Amass, theHarvester, Sublist3r
- 📁 models/ - LLM download script (~170GB)
- 📁 boot/ - Kali ISO + Ventoy

Made by Godman Lab 🧪
