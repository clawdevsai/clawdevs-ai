#!/usr/bin/env python3
"""Validação estática do Dockerfile.base."""

import sys

content = open("Dockerfile.base").read()
lines = content.splitlines()
froms = [l.strip() for l in lines if l.startswith("FROM")]

checks = {
    "FROM usa slim (imagem leve)": "slim" in content,
    "Multi-stage build (>=2 stages)": len(froms) >= 2,
    "PYTHONDONTWRITEBYTECODE=1": "PYTHONDONTWRITEBYTECODE=1" in content,
    "PYTHONUNBUFFERED=1": "PYTHONUNBUFFERED=1" in content,
    "PIP_NO_CACHE_DIR (build enxuto)": "PIP_NO_CACHE_DIR" in content,
    "rm -rf /var/lib/apt/lists (enxuto)": "rm -rf /var/lib/apt/lists" in content,
    "apt-get clean": "apt-get clean" in content,
    "Usuario nao-root (useradd + USER)": "useradd" in content and "USER clawagent" in content,
    "HEALTHCHECK configurado": "HEALTHCHECK" in content,
    "LABEL project (rastreabilidade)": "LABEL project" in content,
    "COPY orchestrator/ e memory/": "COPY orchestrator/" in content and "COPY memory/" in content,
}

print("Stages encontrados:")
for s in froms:
    print(" ", s)
print()
failed = 0
for k, v in checks.items():
    icon = "V" if v else "X"
    print(f"  [{icon}] {k}")
    if not v:
        failed += 1
passed = len(checks) - failed
print(f"\nResultado: {passed}/{len(checks)} checks OK")
sys.exit(0 if failed == 0 else 1)
