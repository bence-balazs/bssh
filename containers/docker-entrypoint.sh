#!/bin/sh

uv sync --frozen
.venv/bin/pyinstaller --onefile bssh.py
mv dist/bssh /data/${FILE_NAME}
chown 1000: /data/*
