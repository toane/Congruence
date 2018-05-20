#!/usr/bin/python3
import sys
import socket

def send(text):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 15556))
        s.sendall(text)


if len(sys.argv) > 1:
    keywords = str.encode(' '.join(sys.argv[1:]))
else:
    keywords = b"trump"

send(keywords)
