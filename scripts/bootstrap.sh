#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
USER_OC_DIR="${HOME}/.config/opencode"
USER_OC_PLUGINS_DIR="${USER_OC_DIR}/plugins"
USER_OC_SKILLS_DIR="${USER_OC_DIR}/skills"

log() {
  printf "[bootstrap] %s\n" "$1"
}

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    printf "[bootstrap] missing required command: %s\n" "$1" >&2
    return 1
  fi
}

select_js_runner() {
  if command -v bunx >/dev/null 2>&1; then
    printf "bunx"
    return 0
  fi

  if command -v npx >/dev/null 2>&1; then
    printf "npx"
    return 0
  fi

  return 1
}

link_file() {
  local src="$1"
  local dst="$2"
  rm -f "$dst"
  ln -s "$src" "$dst"
}

link_dir() {
  local src="$1"
  local dst="$2"
  rm -rf "$dst"
  ln -s "$src" "$dst"
}

install_oh_my_opencode() {
  local runner
  runner="$(select_js_runner)"
  log "Installing oh-my-opencode with ${runner}"
  "${runner}" oh-my-opencode install --no-tui --claude=yes --openai=no --gemini=no --copilot=no
}

ensure_omo_model_config() {
  local template="${ROOT_DIR}/config/oh-my-opencode.json"
  local target="${USER_OC_DIR}/oh-my-opencode.json"

  if [ ! -f "$template" ]; then
    log "No OmO model config template found at config/oh-my-opencode.json — skipping"
    return 0
  fi

  if [ -f "$target" ]; then
    log "OmO model config already exists at ${target} — keeping existing"
  else
    mkdir -p "${USER_OC_DIR}"
    cp "$template" "$target"
    log "Copied OmO model config template to ${target}"
  fi
}

ensure_user_opencode_json() {
  local target="${USER_OC_DIR}/opencode.json"
  local desired='{\n  "plugin": [\n    "oh-my-opencode"\n  ]\n}'
  mkdir -p "${USER_OC_DIR}"

  # Write a deterministic user-level opencode.json matching the project config.
  # Use "oh-my-opencode" (not @latest) for consistency with .opencode/opencode.json.
  if [ ! -f "$target" ]; then
    printf '%b\n' "$desired" > "$target"
    log "Wrote user-level opencode.json at ${target}"
  elif grep -q '"oh-my-opencode@latest"' "$target" 2>/dev/null; then
    # Fix divergence left by OmO installer's @latest suffix
    sed -i '' 's/"oh-my-opencode@latest"/"oh-my-opencode"/' "$target"
    log "Fixed @latest divergence in ${target}"
  else
    log "User-level opencode.json already correct at ${target}"
  fi
}

ensure_repo() {
  if [ ! -d "${ROOT_DIR}/.git" ]; then
    log "Initializing git repository"
    git -C "${ROOT_DIR}" init
  fi
}

ensure_submodules() {
  log "Syncing and initializing submodules"
  git -C "${ROOT_DIR}" submodule sync --recursive
  git -C "${ROOT_DIR}" submodule update --init --recursive
}

install_superpowers_links() {
  mkdir -p "${USER_OC_PLUGINS_DIR}" "${USER_OC_SKILLS_DIR}"

  link_file \
    "${ROOT_DIR}/vendor/superpowers/.opencode/plugins/superpowers.js" \
    "${USER_OC_PLUGINS_DIR}/superpowers.js"

  link_dir \
    "${ROOT_DIR}/vendor/superpowers/skills" \
    "${USER_OC_SKILLS_DIR}/superpowers"

  log "Linked superpowers plugin and skills"
}

install_anthropic_skills() {
  mkdir -p "${USER_OC_SKILLS_DIR}"

  local src_root="${ROOT_DIR}/vendor/anthropic-skills/skills"
  local skill
  for skill in "${src_root}"/*; do
    [ -d "$skill" ] || continue
    local name
    name="$(basename "$skill")"
    link_dir "$skill" "${USER_OC_SKILLS_DIR}/anthropic-${name}"
  done

  log "Linked Anthropic skills into ${USER_OC_SKILLS_DIR}"
}

install_copilot_skills() {
  mkdir -p "${USER_OC_SKILLS_DIR}"

  local src_root="${ROOT_DIR}/vendor/awesome-copilot/skills"
  if [ ! -d "$src_root" ]; then
    log "Skipping Copilot skills (vendor/awesome-copilot not present)"
    return 0
  fi

  local count=0
  local skill
  for skill in "${src_root}"/*; do
    [ -d "$skill" ] || continue
    [ -f "${skill}/SKILL.md" ] || continue
    local name
    name="$(basename "$skill")"
    link_dir "$skill" "${USER_OC_SKILLS_DIR}/copilot-${name}"
    count=$((count + 1))
  done

  log "Linked ${count} Copilot skills into ${USER_OC_SKILLS_DIR}"
}

install_openspec() {
  if ! command -v npm >/dev/null 2>&1 && ! command -v npx >/dev/null 2>&1; then
    log "Skipping OpenSpec install (npm/npx not found)"
    return 0
  fi

  # Try global install first; fall back to npx if it fails (e.g. restricted systems)
  local openspec_cmd=""
  if command -v npm >/dev/null 2>&1; then
    log "Installing OpenSpec CLI globally"
    if npm install -g @fission-ai/openspec@latest 2>/dev/null; then
      openspec_cmd="openspec"
    else
      log "Global install failed — will use npx as fallback"
    fi
  fi

  if [ -z "$openspec_cmd" ] && command -v npx >/dev/null 2>&1; then
    openspec_cmd="npx -y @fission-ai/openspec@latest"
  fi

  if [ -n "$openspec_cmd" ]; then
    log "Initializing OpenSpec for OpenCode"
    (cd "${ROOT_DIR}" && $openspec_cmd init --tools opencode) || {
      log "OpenSpec init failed — you can run 'openspec init --tools opencode' manually"
    }
  else
    log "Skipping OpenSpec init (no working install method found)"
  fi
}

install_custom_skills() {
  mkdir -p "${USER_OC_SKILLS_DIR}"

  local src_root="${ROOT_DIR}/skills/custom"
  local skill
  for skill in "${src_root}"/*; do
    [ -d "$skill" ] || continue
    [ -f "${skill}/SKILL.md" ] || continue
    local name
    name="$(basename "$skill")"
    link_dir "$skill" "${USER_OC_SKILLS_DIR}/custom-${name}"
  done

  log "Linked custom skills into ${USER_OC_SKILLS_DIR}"
}

copy_profile() {
  mkdir -p "${ROOT_DIR}/.opencode"
  cp "${ROOT_DIR}/profiles/daily-dev.jsonc" "${ROOT_DIR}/.opencode/oh-my-opencode.jsonc"
  log "Applied daily-dev profile"
}

generate_registry() {
  if command -v python3 >/dev/null 2>&1; then
    log "Generating registry.yaml and CATALOG.md"
    python3 "${ROOT_DIR}/scripts/gen-registry.py"
    python3 "${ROOT_DIR}/scripts/gen-catalog.py"
  else
    log "Skipping registry generation (python3 not found)"
  fi
}

main() {
  require_cmd git
  ensure_repo
  ensure_submodules

  if select_js_runner >/dev/null 2>&1; then
    install_oh_my_opencode
  else
    log "Skipping oh-my-opencode install (bunx/npx not found)"
  fi

  ensure_omo_model_config
  ensure_user_opencode_json
  install_superpowers_links
  install_anthropic_skills
  install_copilot_skills
  install_custom_skills
  install_openspec
  copy_profile

  generate_registry

  if [ -x "${ROOT_DIR}/scripts/doctor.sh" ]; then
    "${ROOT_DIR}/scripts/doctor.sh"
  fi

  log "Bootstrap complete"
}

main "$@"
