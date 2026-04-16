#!/bin/sh

if [ ! -d "./venv" ]; then
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install discord.py[voice] pynacl
    python3 ./simian.py
else
    source venv/bin/activate
    python3 ./simian.py
fi
