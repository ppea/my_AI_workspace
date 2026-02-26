#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
USER_OC_SKILLS_DIR="${HOME}/.config/opencode/skills"
SRC_ROOT="${ROOT_DIR}/vendor/anthropic-skills/skills"

if [ ! -d "${SRC_ROOT}" ]; then
  printf "[anthropic] missing source directory: %s\n" "${SRC_ROOT}" >&2
  exit 1
fi

mkdir -p "${USER_OC_SKILLS_DIR}"

for skill in "${SRC_ROOT}"/*; do
  [ -d "$skill" ] || continue
  name="$(basename "$skill")"
  dst="${USER_OC_SKILLS_DIR}/anthropic-${name}"
  rm -rf "$dst"
  ln -s "$skill" "$dst"
  printf "[anthropic] linked: %s -> %s\n" "$dst" "$skill"
done

printf "[anthropic] All skills linked\n"
