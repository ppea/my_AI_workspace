#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="${ROOT_DIR}/.opencode/oh-my-opencode.jsonc"

if [ "$#" -ne 1 ]; then
  printf "Usage: %s <minimal|daily-dev|full-stack>\n" "$0" >&2
  exit 1
fi

PROFILE_NAME="$1"
PROFILE_FILE="${ROOT_DIR}/profiles/${PROFILE_NAME}.jsonc"

if [ ! -f "${PROFILE_FILE}" ]; then
  printf "Unknown profile: %s\n" "${PROFILE_NAME}" >&2
  exit 1
fi

mkdir -p "${ROOT_DIR}/.opencode"
cp "${PROFILE_FILE}" "${TARGET}"
printf "[profile] Applied profile: %s\n" "${PROFILE_NAME}"
