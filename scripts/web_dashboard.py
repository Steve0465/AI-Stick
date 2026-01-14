#!/usr/bin/env python3
"""
Web Dashboard for AI_STICK
Access from iPhone Safari for easy interface

Run on Pi: python3 web_dashboard.py
Access: http://[TAILSCALE_IP]:5000
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import subprocess
import os
import shlex
from pathlib import Path
from urllib.parse import parse_qs, urlparse
import socket

PORT = 5000
STICK = Path("/media/ai_stick") if Path("/media/ai_stick").exists() else Path("/Volumes/AI_STICK")


def run_command(cmd):
    """Run shell command and return output."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=30
        )
        return result.stdout or result.stderr
    except Exception as e:
        return f"Error: {e}"


def get_status():
    """Get system status."""
    status = {}

    # Tailscale
    ts_ip = run_command("tailscale ip -4 2>/dev/null").strip()
    status['tailscale'] = ts_ip if ts_ip else "Not connected"

    # Ollama
    ollama_status = run_command("systemctl is-active ollama 2>/dev/null").strip()
    status['ollama'] = "✅ Running" if ollama_status == "active" else "❌ Stopped"

    # Models
    models = run_command("ollama list 2>/dev/null | tail -n +2 | awk '{print $1}'")
    status['models'] = [m for m in models.split('\n') if m]

    # Kiwix
    kiwix_status = run_command("systemctl is-active kiwix 2>/dev/null").strip()
    status['kiwix'] = "✅ Running" if kiwix_status == "active" else "❌ Stopped"

    # Storage
    if STICK.exists():
        df = run_command(f"df -h {STICK} | tail -1")
        parts = df.split()
        if len(parts) >= 5:
            status['storage'] = {
                'total': parts[1],
                'used': parts[2],
                'free': parts[3],
                'percent': parts[4]
            }

    # System
    status['hostname'] = socket.gethostname()
    status['uptime'] = run_command("uptime -p").strip()

    return status


def ask_ollama(prompt, model="phi3:mini"):
    """Ask Ollama a question."""
    # Use json.dumps to properly escape the prompt and model
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False
    })
    cmd = f"curl -s http://localhost:11434/api/generate -d {shlex.quote(payload)}"
    result = run_command(cmd)
    try:
        data = json.loads(result)
        return data.get('response', 'No response')
    except:
        return f"Error: {result}"


class DashboardHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """Handle GET requests."""
        parsed = urlparse(self.path)

        if parsed.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.get_main_page().encode())

        elif parsed.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            status = get_status()
            self.wfile.write(json.dumps(status).encode())

        elif parsed.path == '/api/knowledge':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            knowledge = []
            if STICK.exists():
                for folder in (STICK / "knowledge").iterdir():
                    if folder.is_dir():
                        size = run_command(f"du -sh {folder} 2>/dev/null | cut -f1").strip()
                        knowledge.append({"name": folder.name, "size": size})
            self.wfile.write(json.dumps(knowledge).encode())

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        """Handle POST requests."""
        if self.path == '/api/ask':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())

            prompt = data.get('prompt', '')
            model = data.get('model', 'phi3:mini')

            response = ask_ollama(prompt, model)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'response': response}).encode())

        else:
            self.send_response(404)
            self.end_headers()

    def get_main_page(self):
        """Generate main dashboard HTML."""
        return '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI_STICK Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #0d1117;
            color: #c9d1d9;
            padding: 20px;
            line-height: 1.6;
        }
        .container { max-width: 800px; margin: 0 auto; }
        h1 {
            font-size: 2em;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .card {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }
        .card h2 {
            font-size: 1.3em;
            margin-bottom: 15px;
            color: #58a6ff;
        }
        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }
        .status-item {
            background: #0d1117;
            padding: 15px;
            border-radius: 6px;
            border: 1px solid #21262d;
        }
        .status-item strong { color: #8b949e; display: block; margin-bottom: 5px; }
        .status-item span { color: #58a6ff; font-size: 1.1em; }
        button {
            background: #238636;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            font-size: 16px;
            cursor: pointer;
            width: 100%;
            margin-top: 10px;
        }
        button:hover { background: #2ea043; }
        button:disabled { background: #30363d; cursor: not-allowed; }
        input, textarea, select {
            width: 100%;
            padding: 12px;
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 6px;
            color: #c9d1d9;
            font-size: 16px;
            margin-bottom: 10px;
        }
        textarea { resize: vertical; min-height: 100px; font-family: inherit; }
        .response {
            background: #0d1117;
            padding: 15px;
            border-radius: 6px;
            border: 1px solid #30363d;
            margin-top: 15px;
            white-space: pre-wrap;
            font-family: 'SF Mono', Monaco, monospace;
            font-size: 14px;
            line-height: 1.6;
        }
        .loading { opacity: 0.6; }
        .list { list-style: none; }
        .list li {
            padding: 10px;
            background: #0d1117;
            margin: 8px 0;
            border-radius: 6px;
            border: 1px solid #21262d;
        }
        .list li strong { color: #58a6ff; }
        .emoji { font-size: 1.2em; margin-right: 8px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 AI_STICK Dashboard</h1>
        <p style="color: #8b949e; margin-bottom: 20px;">Control your portable AI server</p>

        <!-- Status -->
        <div class="card">
            <h2>📊 System Status</h2>
            <div class="status-grid" id="status">
                <div class="status-item">
                    <strong>Loading...</strong>
                </div>
            </div>
        </div>

        <!-- AI Chat -->
        <div class="card">
            <h2>💬 Ask AI</h2>
            <select id="model">
                <option value="phi3:mini">phi3:mini (Fast)</option>
                <option value="tinyllama">tinyllama (Faster)</option>
                <option value="qwen2.5:3b">qwen2.5:3b (Code)</option>
            </select>
            <textarea id="prompt" placeholder="Ask me anything..."></textarea>
            <button onclick="askAI()">Send Question</button>
            <div id="ai-response" class="response" style="display: none;"></div>
        </div>

        <!-- Knowledge -->
        <div class="card">
            <h2>📚 Offline Knowledge</h2>
            <ul id="knowledge" class="list">
                <li>Loading...</li>
            </ul>
            <a href="http://localhost:8080" target="_blank">
                <button>Open Kiwix (Wikipedia)</button>
            </a>
        </div>

        <!-- Quick Actions -->
        <div class="card">
            <h2>🚀 Quick Actions</h2>
            <button onclick="refreshAll()">🔄 Refresh All</button>
        </div>
    </div>

    <script>
        function loadStatus() {
            fetch('/api/status')
                .then(r => r.json())
                .then(data => {
                    const html = `
                        <div class="status-item">
                            <strong>🔗 Tailscale</strong>
                            <span>${data.tailscale}</span>
                        </div>
                        <div class="status-item">
                            <strong>🧠 Ollama</strong>
                            <span>${data.ollama}</span>
                        </div>
                        <div class="status-item">
                            <strong>📚 Kiwix</strong>
                            <span>${data.kiwix}</span>
                        </div>
                        <div class="status-item">
                            <strong>💾 Storage</strong>
                            <span>${data.storage ? data.storage.used + ' / ' + data.storage.total : 'N/A'}</span>
                        </div>
                        <div class="status-item">
                            <strong>⏱ Uptime</strong>
                            <span>${data.uptime}</span>
                        </div>
                        <div class="status-item">
                            <strong>🤖 Models</strong>
                            <span>${data.models ? data.models.length : 0}</span>
                        </div>
                    `;
                    document.getElementById('status').innerHTML = html;

                    // Update model selector
                    if (data.models && data.models.length > 0) {
                        const select = document.getElementById('model');
                        select.innerHTML = data.models.map(m =>
                            `<option value="${m}">${m}</option>`
                        ).join('');
                    }
                });
        }

        function loadKnowledge() {
            fetch('/api/knowledge')
                .then(r => r.json())
                .then(data => {
                    const html = data.map(k =>
                        `<li><strong>${k.name}</strong> - ${k.size}</li>`
                    ).join('');
                    document.getElementById('knowledge').innerHTML = html || '<li>No knowledge bases found</li>';
                });
        }

        function askAI() {
            const prompt = document.getElementById('prompt').value;
            const model = document.getElementById('model').value;
            const responseDiv = document.getElementById('ai-response');

            if (!prompt.trim()) return;

            responseDiv.style.display = 'block';
            responseDiv.textContent = '🤔 Thinking...';
            responseDiv.classList.add('loading');

            fetch('/api/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({prompt, model})
            })
            .then(r => r.json())
            .then(data => {
                responseDiv.classList.remove('loading');
                responseDiv.textContent = data.response;
            })
            .catch(err => {
                responseDiv.classList.remove('loading');
                responseDiv.textContent = 'Error: ' + err;
            });
        }

        function refreshAll() {
            loadStatus();
            loadKnowledge();
        }

        // Auto-refresh status every 10 seconds
        setInterval(loadStatus, 10000);

        // Initial load
        loadStatus();
        loadKnowledge();

        // Enter key to send
        document.getElementById('prompt').addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && e.metaKey) {
                askAI();
            }
        });
    </script>
</body>
</html>'''

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass


def main():
    print("╔════════════════════════════════════════════════════════╗")
    print("║           🌐 AI_STICK WEB DASHBOARD                    ║")
    print("╚════════════════════════════════════════════════════════╝")
    print("")

    # Get IPs
    hostname = socket.gethostname()

    try:
        # Try to get Tailscale IP
        ts_ip = run_command("tailscale ip -4 2>/dev/null").strip()
        if ts_ip:
            print(f"🔗 Tailscale IP: {ts_ip}")
            print(f"   Access from iPhone: http://{ts_ip}:{PORT}")
    except:
        pass

    # Local IP
    try:
        local_ip = socket.gethostbyname(hostname)
        print(f"🏠 Local IP: {local_ip}")
        print(f"   Local access: http://{local_ip}:{PORT}")
    except:
        pass

    print(f"\n✅ Server running on port {PORT}")
    print("📱 Open in Safari on iPhone to access dashboard")
    print("⌨️  Press Ctrl+C to stop")
    print("")

    server = HTTPServer(('0.0.0.0', PORT), DashboardHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")
        server.shutdown()


if __name__ == "__main__":
    main()
