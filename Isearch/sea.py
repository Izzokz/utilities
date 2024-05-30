import argparse
import subprocess

keys = [
    "What is ",
    "How to ",
    "Purposes of ",
    "How popular is ",
    "Cost of "
]

def search(text):
    search = "https://www.google.com/search?client=firefox-b-lm&q="
    for key in keys:
        subprocess.run(["firefox", search + key + text], capture_output = True, text = True, check = True)

parser = argparse.ArgumentParser()
parser.add_argument('search', type = str)
try:
    search(parser.parse_args().search)
except:
    subprocess.run([f"python3 {__file__.split('/')[-1]} {'-'.join(input('What kind of information do you want?').split())}"], shell = True)
