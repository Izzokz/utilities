import subprocess
import time
import os

keys = [
    "What+is+",
    "How+to+",
    "Purposes+of+",
    "How+popular+is+",
    "Cost+of+"
]

device = os.name

def search(text):
    search = "https://www.google.com/search?q="
    
    if device == 'posix':
        if subprocess.run(['ps aux | grep -q [f]irefox && echo "on" || echo "off"'], capture_output = True, shell = True).stdout == b'off\n':
            timer = True
        for key in keys:
            subprocess.run(["firefox " + search + key + text + " 2>/dev/null"], shell = True)
            if timer:
                time.sleep(1)
                timer = False
    
    if device == 'nt':
        if subprocess.run(["PowerShell", "Get-Process firefox -ErrorAction SilentlyContinue"], capture_output = True, shell = True).stdout == b'':
            timer = True
        for key in keys:
            subprocess.run(["PowerShell", "start firefox " + search + key + text], shell = True)
            if timer:
                time.sleep(1)
                timer = False

query = "+".join(input("What kind of information do you want?").split())
search(query)