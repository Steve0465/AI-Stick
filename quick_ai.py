 #!/usr/bin/env python3
  import requests
  import sys

  question = ' '.join(sys.argv[1:])
  if not question:
      print("Usage: ./quick_ai.py 'your question'")
      sys.exit(1)

  print("🤖 Asking Mistral...\n")
  response = requests.post('http://localhost:11434/api/generate',
      json={
          "model": "mistral",
          "prompt": question + "\n\nAnswer briefly in 2-3 sentences.",
          "stream": False
      })

  print(response.json()['response'])

