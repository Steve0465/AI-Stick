# 📱 iPhone Shortcuts - One-Tap AI Access

Make AI_STICK even easier - just tap your phone!

---

## 🚀 Create "AI_STICK" Shortcut

### Step 1: Open Shortcuts App

On your iPhone, open the **Shortcuts** app (comes with iOS).

### Step 2: Create New Shortcut

1. Tap **"+"** (top right)
2. Tap **"Add Action"**
3. Search for **"Run Script Over SSH"**
4. Select it

### Step 3: Configure

Fill in these fields:

**Host:** `aiserver.local` (or `100.100.32.58`)
**Port:** `22`
**User:** `pi`
**Password:** (your Pi password)
**Script:**
```bash
cd /media/pi/AI_STICK && ./START
```

### Step 4: Name It

Tap **"AI_STICK"** at the top and name it: **"AI_STICK"**

### Step 5: Add to Home Screen

1. Tap the settings icon (three dots)
2. Tap **"Add to Home Screen"**
3. Choose an icon (⚡ or 🤖 looks cool)
4. Tap **"Add"**

---

## 🎯 Now You Have One-Tap Access!

Just tap the **AI_STICK** icon on your home screen!

It will:
- SSH into your Pi
- Navigate to AI_STICK
- Show the menu
- All in Terminus or Safari

---

## 🔥 More Shortcuts You Can Create

### "Ask AI" - Voice to AI

1. New Shortcut
2. Add: **"Dictate Text"**
3. Add: **"Run Script Over SSH"**
4. Script:
```bash
cd /media/pi/AI_STICK && ./quick_ai.py "YOUR_QUESTION_HERE"
```
5. Replace `YOUR_QUESTION_HERE` with: **"Dictated Text"** (from previous step)

**Now:** Say "Hey Siri, Ask AI" → speak your question → get answer!

---

### "Code Generator" - Quick Code

1. New Shortcut
2. Add: **"Ask for Input"** (prompt: "What do you want to build?")
3. Add: **"Run Script Over SSH"**
4. Script:
```bash
cd /media/pi/AI_STICK && ./code_writer.py "PROVIDED_INPUT"
```

**Tap → Type what you want → Get code!**

---

### "System Check" - One Tap Status

1. New Shortcut
2. Add: **"Run Script Over SSH"**
3. Script:
```bash
cd /media/pi/AI_STICK && ./check_system.sh
```

**Quick health check!**

---

## 💡 Pro Tip: Siri Integration

For any shortcut:
1. Edit shortcut
2. Tap settings (three dots)
3. Enable **"Show in Share Sheet"**
4. Enable **"Add to Siri"**
5. Record phrase like: "Start AI" or "Ask my AI"

**Then:** "Hey Siri, Start AI" → Menu appears!

---

## 🎮 My Recommended Setup

Create these 3 shortcuts on your home screen:

1. **🤖 AI_STICK** - Main menu
2. **💬 Ask AI** - Voice questions
3. **📝 Code It** - Generate code

**Everything else** you can access through the main menu.

---

## 📸 Screenshot Your Cheat Sheet

Take a screenshot of `CHEAT_SHEET.txt` and set as:
- Lock screen wallpaper
- OR save to Photos → "Favorites"
- OR print and tape to laptop

**Never forget the commands!**

---

## ⚡ The Lazy Way (What I'd Do)

**Just create ONE shortcut:**

Name: **"AI"**
Icon: 🤖
Action: SSH → `cd /media/pi/AI_STICK && ./START`
Add to: Home screen

**Then just tap it.** Menu does everything else.

Literally:
1. Tap 🤖
2. Pick from menu
3. Done

**That's it.** No memorizing shit. 🔥

---

## 🆘 Troubleshooting Shortcuts

**"Authentication failed"**
- Make sure you saved Pi password in Shortcuts
- Or use Terminus app instead (already authenticated)

**"Host not found"**
- Use IP instead: `100.100.32.58`
- Or make sure Tailscale is connected

**"Script failed"**
- Check that AI_STICK is plugged into Pi
- Run: `ls /media/pi/AI_STICK` to verify

---

## 🔥 Bottom Line

**You only need ONE shortcut:**

SSH to Pi → run `./START` → Pick from menu

**Everything else is just extra convenience.**

Make it. Use it. Forget everything else. 💪
