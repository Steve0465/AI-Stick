# 🤖 Interactive Coding Agent with Mistral

Your personal AI coding assistant. Talk naturally, iterate on code, test instantly.

## 🚀 Quick Start

```bash
cd /media/pi/AI_STICK
./coding_agent.py
```

That's it! You're now chatting with Mistral.

---

## 💬 How to Use

Just talk naturally:

```
💬 You: write a Python script that backs up a directory
🤖 Mistral: [writes code]

💬 You: add error handling
🤖 Mistral: [improves code]

💬 You: save
💾 Save as: backup.py
✅ Saved and made executable: backup.py

💬 You: run
🚀 Running backup.py...
[output shown]

💬 You: exit
```

---

## 🎯 Example Conversations

### Example 1: Build a Tool

```
You: write a bash script that shows disk space for all drives
Mistral: [writes script]

You: make it colorful with ANSI colors
Mistral: [adds colors]

You: save
Save as: diskspace.sh

You: run
[shows output]

You: perfect!
```

### Example 2: Debug Code

```
You: here's my code [paste code]. why isn't it working?
Mistral: [analyzes and explains]

You: how do I fix it?
Mistral: [provides fixed version]

You: save
```

### Example 3: Learn by Doing

```
You: explain how to use asyncio in Python with an example
Mistral: [explains with code]

You: can you make that example do web scraping?
Mistral: [expands example]

You: save
```

---

## 🎮 Commands

While chatting, you can use these commands:

| Command | What it does |
|---------|-------------|
| `save` | Save the last code Mistral wrote |
| `run` | Execute the saved code |
| `show` | Display the current code |
| `clear` | Start fresh (clear history) |
| `exit` or `quit` | End session |

---

## 🔥 Power Tips

### 1. Iterate Freely

```
You: write a file sorter
Mistral: [writes basic version]

You: add logging
You: now make it work recursively
You: add a progress bar
You: perfect, save
```

### 2. Learn as You Go

```
You: I don't understand how decorators work in Python
Mistral: [explains with examples]

You: show me a real use case
Mistral: [provides practical example]
```

### 3. Quick Prototypes

```
You: write a web server that shows system stats
Mistral: [writes Flask app]

You: save
You: run
[test it in browser]
```

### 4. Code Review

```
You: review this code for security issues [paste code]
Mistral: [analyzes and suggests improvements]

You: rewrite it with those fixes
Mistral: [provides secure version]
```

---

## 🛠️ Advanced Usage

### Multi-File Projects

```
You: write a Python module for config management
Mistral: [writes config.py]

You: save
Save as: config.py

You: now write a main script that uses it
Mistral: [writes main.py]

You: save
Save as: main.py
```

### Language Mixing

```
You: write a bash script that calls a Python script
Mistral: [writes both]

You: save the bash part as wrapper.sh
You: [chat continues]
You: save the Python part as worker.py
```

### Testing Code

```
You: write a function that validates email addresses
Mistral: [writes function]

You: write unit tests for that
Mistral: [writes tests]

You: save
You: run
[tests execute]
```

---

## 📋 Use Cases

### System Administration

```
You: write a script that monitors CPU and alerts if over 80%
You: add email notifications
You: save and run
```

### Data Processing

```
You: write a CSV parser that finds duplicates
You: make it handle large files efficiently
You: add a progress bar
```

### Web Development

```
You: write a REST API for a todo list
You: add authentication
You: include error handling
```

### Automation

```
You: write a script that organizes downloads by file type
You: make it run on a schedule
You: add logging
```

---

## 🐛 Troubleshooting

### "Cannot connect to Ollama"

```bash
# Check if Ollama is running
sudo systemctl status ollama

# Start it
sudo systemctl start ollama

# Check models
ollama list
```

### "Mistral model not found"

```bash
# Download Mistral
ollama pull mistral

# Verify
ollama list
```

### Code won't execute

```bash
# Make sure file is executable
chmod +x yourfile.py

# Check Python path
which python3

# Test manually
python3 yourfile.py
```

### Want to use a different model?

Edit `coding_agent.py` and change this line:
```python
"model": "mistral",  # Change to "phi3:mini" or "codellama"
```

---

## 🎯 Best Practices

### 1. Be Specific

❌ Bad: "write a script"
✅ Good: "write a Python script that backs up /home to /backup with timestamps"

### 2. Iterate Incrementally

Build features one at a time:
1. Basic functionality
2. Error handling
3. User interface
4. Optimization

### 3. Test as You Go

After each change:
- Save the code
- Run it
- Verify it works
- Then add the next feature

### 4. Ask Questions

Don't understand something? Just ask:
- "explain what this line does"
- "why did you use this approach?"
- "what are the alternatives?"

---

## 🔥 Real Examples

### Build a System Monitor

```
Session transcript:

You: write a Python script that shows CPU, RAM, and disk usage
Mistral: [writes basic version]

You: add colors - red for >80%, yellow for >60%, green otherwise
Mistral: [adds colored output]

You: make it refresh every 2 seconds like htop
Mistral: [adds loop with clear screen]

You: add network bandwidth monitoring
Mistral: [adds network stats]

You: save
Save as: sysmon.py

You: run
[beautiful colored system monitor runs]
```

### Create a Backup Tool

```
You: write a bash script that backs up a directory to a timestamped tar.gz
Mistral: [writes script]

You: add verification that backup succeeded
Mistral: [adds checksum verification]

You: keep only the last 7 backups, delete older ones
Mistral: [adds cleanup logic]

You: save as backup.sh and run
[creates backup successfully]
```

---

## 📖 Learning Path

### Beginner

Start with simple scripts:
1. "write a hello world script"
2. "write a script that lists files"
3. "add error handling to that"

### Intermediate

Build real tools:
1. "write a file organizer"
2. "write a web scraper"
3. "write a system monitoring tool"

### Advanced

Complex projects:
1. "write a REST API with authentication"
2. "write a distributed task queue"
3. "write a CI/CD pipeline script"

---

## 🚀 Pro Workflows

### Workflow 1: Rapid Prototyping

```
1. Describe what you want
2. Review the code
3. Ask for changes
4. Iterate until perfect
5. Save and test
6. Deploy
```

### Workflow 2: Learning New Tech

```
1. "explain [technology] with examples"
2. "show me a real use case"
3. "write a complete project using it"
4. Study the code
5. Ask questions about specific parts
6. Modify and experiment
```

### Workflow 3: Debug Existing Code

```
1. Paste your code
2. "what's wrong with this?"
3. Get explanation
4. "fix it"
5. Compare versions
6. Learn from differences
```

---

## 💡 Remember

- **Conversation is natural** - talk like you're pair programming
- **Iterate freely** - change your mind, refine ideas
- **Test frequently** - save and run to verify
- **Ask questions** - Mistral explains anything
- **Build incrementally** - start simple, add features

---

## 🎓 Next Steps

Once comfortable with the coding agent:

1. **Integrate with other tools**
   ```
   ./coding_agent.py  # Write code
   ./smart_ai.py      # Query knowledge base
   ./ai_agent.py      # Analyze existing files
   ```

2. **Build a project library**
   - Save your best scripts
   - Create a personal toolkit
   - Share with others

3. **Customize the agent**
   - Edit prompts
   - Add new commands
   - Extend functionality

---

**Your AI pair programmer is ready. Start coding!** 🔥

```bash
./coding_agent.py
```
