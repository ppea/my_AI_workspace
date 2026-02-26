#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
USER_OC_SKILLS_DIR="${HOME}/.config/opencode/skills"
SRC_ROOT="${ROOT_DIR}/vendor/awesome-copilot/skills"

if [ ! -d "${SRC_ROOT}" ]; then
  printf "[copilot] missing source directory: %s\n" "${SRC_ROOT}" >&2
  exit 1
fi

mkdir -p "${USER_OC_SKILLS_DIR}"

count=0
for skill in "${SRC_ROOT}"/*; do
  [ -d "$skill" ] || continue
  # Only link directories that contain a SKILL.md
  [ -f "${skill}/SKILL.md" ] || continue
  name="$(basename "$skill")"
  dst="${USER_OC_SKILLS_DIR}/copilot-${name}"
  rm -rf "$dst"
  ln -s "$skill" "$dst"
  count=$((count + 1))
done

printf "[copilot] Linked %d skills into %s\n" "$count" "${USER_OC_SKILLS_DIR}"
