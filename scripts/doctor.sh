#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
USER_OC_DIR="${HOME}/.config/opencode"

ok() {
  printf "[doctor] OK: %s\n" "$1"
}

warn() {
  printf "[doctor] WARN: %s\n" "$1"
}

check_cmd() {
  local cmd="$1"
  if command -v "$cmd" >/dev/null 2>&1; then
    ok "command found: ${cmd}"
  else
    warn "command missing: ${cmd}"
  fi
}

check_path_exists() {
  local path="$1"
  if [ -e "$path" ]; then
    ok "exists: ${path}"
  else
    warn "missing: ${path}"
  fi
}

check_symlink_target() {
  local path="$1"
  if [ -L "$path" ]; then
    ok "symlink present: ${path} -> $(readlink "$path")"
  elif [ -e "$path" ]; then
    warn "not a symlink: ${path}"
  else
    warn "missing symlink: ${path}"
  fi
}

main() {
  check_cmd git
  check_cmd opencode
  check_cmd bunx
  check_cmd npx
  check_cmd node
  check_cmd npm
  check_cmd openspec

  check_path_exists "${ROOT_DIR}/.git"
  check_path_exists "${ROOT_DIR}/.gitmodules"
  check_path_exists "${ROOT_DIR}/.opencode/opencode.json"
  check_path_exists "${ROOT_DIR}/.opencode/oh-my-opencode.jsonc"
  check_path_exists "${ROOT_DIR}/profiles/minimal.jsonc"
  check_path_exists "${ROOT_DIR}/profiles/daily-dev.jsonc"
  check_path_exists "${ROOT_DIR}/profiles/full-stack.jsonc"
  check_path_exists "${ROOT_DIR}/config/oh-my-opencode.json"

  check_path_exists "${ROOT_DIR}/vendor/oh-my-opencode"
  check_path_exists "${ROOT_DIR}/vendor/superpowers"
  check_path_exists "${ROOT_DIR}/vendor/anthropic-skills"
  check_path_exists "${ROOT_DIR}/vendor/awesome-copilot"
  check_path_exists "${ROOT_DIR}/vendor/openspec"

  check_symlink_target "${USER_OC_DIR}/plugins/superpowers.js"
  check_symlink_target "${USER_OC_DIR}/skills/superpowers"

  # Anthropic skill symlinks
  local anthropic_count=0
  for skill in "${USER_OC_DIR}/skills"/anthropic-*; do
    [ -L "$skill" ] && anthropic_count=$((anthropic_count + 1))
  done
  if [ "$anthropic_count" -gt 0 ]; then
    ok "anthropic skills linked: ${anthropic_count} found"
  else
    warn "no anthropic skill symlinks in ${USER_OC_DIR}/skills/"
  fi

  # Copilot skill symlinks (awesome-copilot)
  local copilot_count=0
  for skill in "${USER_OC_DIR}/skills"/copilot-*; do
    [ -L "$skill" ] && copilot_count=$((copilot_count + 1))
  done
  if [ "$copilot_count" -gt 0 ]; then
    ok "copilot skills linked: ${copilot_count} found"
  else
    warn "no copilot skill symlinks in ${USER_OC_DIR}/skills/"
  fi

  # OpenSpec generated assets
  check_path_exists "${ROOT_DIR}/.opencode/skills/openspec-propose"
  check_path_exists "${ROOT_DIR}/.opencode/command/opsx-propose.md"
  check_path_exists "${ROOT_DIR}/openspec"

  # OmO user-level config (written by installer)
  check_path_exists "${USER_OC_DIR}/oh-my-opencode.json"

  # Superpowers plugin file resolves
  if [ -L "${USER_OC_DIR}/plugins/superpowers.js" ]; then
    local target
    target="$(readlink "${USER_OC_DIR}/plugins/superpowers.js")"
    if [ -f "$target" ]; then
      ok "superpowers plugin target exists: ${target}"
    else
      warn "superpowers plugin target BROKEN: ${target}"
    fi
  fi

  # Registry and catalog
  check_path_exists "${ROOT_DIR}/registry.yaml"
  check_path_exists "${ROOT_DIR}/CATALOG.md"
  if command -v python3 >/dev/null 2>&1 && [ -f "${ROOT_DIR}/scripts/gen-registry.py" ]; then
    if python3 "${ROOT_DIR}/scripts/gen-registry.py" --check 2>/dev/null; then
      ok "registry.yaml is up to date"
    else
      warn "registry.yaml is stale — run: python3 scripts/gen-registry.py"
    fi
  fi
  if command -v python3 >/dev/null 2>&1 && [ -f "${ROOT_DIR}/scripts/gen-catalog.py" ]; then
    if python3 "${ROOT_DIR}/scripts/gen-catalog.py" --check 2>/dev/null; then
      ok "CATALOG.md is up to date"
    else
      warn "CATALOG.md is stale — run: python3 scripts/gen-catalog.py"
    fi
  fi

  # Custom skill symlinks
  local custom_count=0
  for skill in "${USER_OC_DIR}/skills"/custom-*; do
    [ -L "$skill" ] && custom_count=$((custom_count + 1))
  done
  if [ "$custom_count" -gt 0 ]; then
    ok "custom skills linked: ${custom_count} found"
  else
    warn "no custom skill symlinks in ${USER_OC_DIR}/skills/"
  fi

  # User-level opencode.json
  check_path_exists "${USER_OC_DIR}/opencode.json"
  if [ -f "${USER_OC_DIR}/opencode.json" ] && grep -q '"oh-my-opencode@latest"' "${USER_OC_DIR}/opencode.json" 2>/dev/null; then
    warn "user opencode.json has @latest suffix — run bootstrap to fix"
  fi

  printf "[doctor] Done\n"
}

main "$@"
