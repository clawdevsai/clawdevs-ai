#!/usr/bin/env bash
# Interactive y/N check for Makefile destructive targets (avoids GNU Make eating $(...) in recipes).
set -euo pipefail
read -r -p "Confirma? [y/N] " confirm || exit 1
confirm=$(printf '%s' "$confirm" | tr -d '\r' | tr '[:upper:]' '[:lower:]')
case "$confirm" in y|yes) exit 0;; *) exit 1;; esac
