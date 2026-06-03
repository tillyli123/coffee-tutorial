import subprocess
import sys
import time
import re
import os

cmd = [
    "ssh", "-o", "StrictHostKeyChecking=no",
    "-o", "ServerAliveInterval=30",
    "-i", os.path.expanduser("~/.ssh/id_ed25519"),
    "-R", "airquality:80:localhost:8080",
    "serveo.net"
]

proc = subprocess.Popen(
    cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

url = "https://airquality.serveo.net"
start = time.time()
timeout = 25

for line in proc.stdout:
    print(line, end='')
    m = re.search(r'(https://airquality\.serveo[a-z]*\.com)', line)
    if m:
        url = m.group(1)
        print(f"\n\n>>> PUBLIC URL: {url}")
        break
    if "already in use" in line.lower():
        print("\n>>> ERROR: Subdomain taken")
        proc.terminate()
        sys.exit(1)
    if time.time() - start > timeout:
        print(f"\n\n>>> TIMEOUT. Using: {url}")
        break

if not url:
    proc.terminate()
    sys.exit(1)

proc.wait()
