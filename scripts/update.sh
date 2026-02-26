#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

printf "[update] Syncing submodule URLs\n"
git -C "${ROOT_DIR}" submodule sync --recursive

printf "[update] Updating submodules to latest remote HEADs\n"
git -C "${ROOT_DIR}" submodule update --init --recursive --remote

if command -v openspec >/dev/null 2>&1; then
  printf "[update] Regenerating OpenSpec assets\n"
  (cd "${ROOT_DIR}" && openspec update)
else
  printf "[update] openspec not found, skipping openspec update\n"
fi

if command -v python3 >/dev/null 2>&1; then
  printf "[update] Regenerating registry.yaml and CATALOG.md\n"
  python3 "${ROOT_DIR}/scripts/gen-registry.py"
  python3 "${ROOT_DIR}/scripts/gen-catalog.py"
else
  printf "[update] python3 not found, skipping registry generation\n"
fi

printf "[update] Done\n"
