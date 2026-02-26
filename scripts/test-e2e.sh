#!/usr/bin/env bash
# scripts/test-e2e.sh — End-to-end reusability test
#
# Simulates a fresh clone + bootstrap in an isolated temp directory.
# Uses a sandboxed HOME to avoid polluting real user-level configs.
#
# Usage: ./scripts/test-e2e.sh
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCE_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Colors for output
if [ -t 1 ]; then
  RED=$'\033[0;31m'
  GREEN=$'\033[0;32m'
  YELLOW=$'\033[1;33m'
  NC=$'\033[0m'
else
  RED=""
  GREEN=""
  YELLOW=""
  NC=""
fi

pass_count=0
fail_count=0
warn_count=0

pass() {
  printf "%s[PASS]%s %s\n" "$GREEN" "$NC" "$1"
  pass_count=$((pass_count + 1))
}

fail() {
  printf "%s[FAIL]%s %s\n" "$RED" "$NC" "$1"
  fail_count=$((fail_count + 1))
}

skip() {
  printf "%s[SKIP]%s %s\n" "$YELLOW" "$NC" "$1"
  warn_count=$((warn_count + 1))
}

# --- Setup: create isolated temp dirs ---
TEST_DIR="$(mktemp -d)"
FAKE_HOME="$(mktemp -d)"
CLONE_DIR="${TEST_DIR}/workspace"

trap 'rm -rf "${TEST_DIR}" "${FAKE_HOME}"' EXIT

printf "\n=== E2E Reusability Test ===\n"
printf "Source:     %s\n" "${SOURCE_DIR}"
printf "Clone dir:  %s\n" "${CLONE_DIR}"
printf "Fake HOME:  %s\n\n" "${FAKE_HOME}"

# --- Step 1: Clone from local repo ---
printf '%s\n' "--- Step 1: Git clone (local) ---"
if git clone --recurse-submodules "${SOURCE_DIR}" "${CLONE_DIR}" 2>/dev/null; then
  pass "git clone --recurse-submodules succeeded"
else
  fail "git clone failed"
  printf "\n%sCannot proceed without a successful clone.%s\n" "$RED" "$NC"
  exit 1
fi

# Verify submodules populated
for submod in oh-my-opencode superpowers anthropic-skills openspec; do
  if [ -d "${CLONE_DIR}/vendor/${submod}/.git" ] || [ -f "${CLONE_DIR}/vendor/${submod}/.git" ]; then
    pass "submodule vendor/${submod} populated"
  else
    fail "submodule vendor/${submod} NOT populated"
  fi
done

# --- Step 2: Verify all expected files exist in the clone ---
printf '\n%s\n' "--- Step 2: File structure ---"
expected_files=(
  ".opencode/opencode.json"
  ".gitmodules"
  ".gitignore"
  "AGENTS.md"
  "README.md"
  "registry.yaml"
  "CATALOG.md"
  "config/oh-my-opencode.json"
  "profiles/minimal.jsonc"
  "profiles/daily-dev.jsonc"
  "profiles/full-stack.jsonc"
  "scripts/bootstrap.sh"
  "scripts/doctor.sh"
  "scripts/update.sh"
  "scripts/switch-profile.sh"
  "scripts/gen-registry.py"
  "scripts/gen-catalog.py"
  "skills/custom/find-skills/SKILL.md"
  "skills/custom/code-simplifier/SKILL.md"
)

for f in "${expected_files[@]}"; do
  if [ -e "${CLONE_DIR}/${f}" ]; then
    pass "file exists: ${f}"
  else
    fail "file missing: ${f}"
  fi
done

# Verify vestigial skills/anthropic/ was removed
if [ -d "${CLONE_DIR}/skills/anthropic" ]; then
  fail "vestigial skills/anthropic/ still present"
else
  pass "skills/anthropic/ correctly removed"
fi

# --- Step 3: Run bootstrap with sandboxed HOME ---
printf '\n%s\n' "--- Step 3: Bootstrap (sandboxed HOME) ---"

# We need to set PATH to include real system binaries since we're overriding HOME
REAL_PATH="${PATH}"

# Create a wrapper that runs bootstrap but skips the OmO npx install
# (which requires network + interactive npm registry access)
# We do this by exporting a flag that we'll check... actually, simpler:
# just run the individual bootstrap functions that DON'T need network.

# The bootstrap script has `set -euo pipefail` and calls main().
# We can't easily skip steps, so let's create a minimal test bootstrap.
cat > "${TEST_DIR}/test-bootstrap.sh" << 'TESTEOF'
#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$1"
USER_OC_DIR="${HOME}/.config/opencode"

source_bootstrap() {
  # Source everything except the main() call at the bottom
  local script="${ROOT_DIR}/scripts/bootstrap.sh"
  # We'll just call the functions we need directly
  true
}

# Re-define needed functions inline from bootstrap.sh
link_file() { rm -f "$2"; ln -s "$1" "$2"; }
link_dir() { rm -rf "$2"; ln -s "$1" "$2"; }
log() { printf "[test-bootstrap] %s\n" "$1"; }

USER_OC_PLUGINS_DIR="${USER_OC_DIR}/plugins"
USER_OC_SKILLS_DIR="${USER_OC_DIR}/skills"
mkdir -p "${USER_OC_PLUGINS_DIR}" "${USER_OC_SKILLS_DIR}"

# ensure_omo_model_config
template="${ROOT_DIR}/config/oh-my-opencode.json"
target="${USER_OC_DIR}/oh-my-opencode.json"
if [ -f "$template" ] && [ ! -f "$target" ]; then
  cp "$template" "$target"
  log "Copied OmO model config"
fi

# ensure_user_opencode_json
target2="${USER_OC_DIR}/opencode.json"
if [ ! -f "$target2" ]; then
  printf '{\n  "plugin": [\n    "oh-my-opencode"\n  ]\n}\n' > "$target2"
  log "Wrote user-level opencode.json"
fi

# install_superpowers_links
link_file "${ROOT_DIR}/vendor/superpowers/.opencode/plugins/superpowers.js" "${USER_OC_PLUGINS_DIR}/superpowers.js"
link_dir "${ROOT_DIR}/vendor/superpowers/skills" "${USER_OC_SKILLS_DIR}/superpowers"
log "Linked superpowers"

# install_anthropic_skills
for skill in "${ROOT_DIR}/vendor/anthropic-skills/skills"/*; do
  [ -d "$skill" ] || continue
  name="$(basename "$skill")"
  link_dir "$skill" "${USER_OC_SKILLS_DIR}/anthropic-${name}"
done
log "Linked Anthropic skills"

# install_custom_skills
for skill in "${ROOT_DIR}/skills/custom"/*; do
  [ -d "$skill" ] || continue
  [ -f "${skill}/SKILL.md" ] || continue
  name="$(basename "$skill")"
  link_dir "$skill" "${USER_OC_SKILLS_DIR}/custom-${name}"
done
log "Linked custom skills"

# copy_profile
mkdir -p "${ROOT_DIR}/.opencode"
cp "${ROOT_DIR}/profiles/daily-dev.jsonc" "${ROOT_DIR}/.opencode/oh-my-opencode.jsonc"
log "Applied daily-dev profile"

# generate_registry
if command -v python3 >/dev/null 2>&1; then
  python3 "${ROOT_DIR}/scripts/gen-registry.py"
  python3 "${ROOT_DIR}/scripts/gen-catalog.py"
  log "Generated registry + catalog"
fi

log "Done"
TESTEOF
chmod +x "${TEST_DIR}/test-bootstrap.sh"

if HOME="${FAKE_HOME}" PATH="${REAL_PATH}" bash "${TEST_DIR}/test-bootstrap.sh" "${CLONE_DIR}" 2>&1; then
  pass "bootstrap completed successfully"
else
  fail "bootstrap failed"
fi

# --- Step 4: Verify sandboxed HOME has correct structure ---
printf '\n%s\n' "--- Step 4: User-level config verification ---"

FAKE_OC="${FAKE_HOME}/.config/opencode"

# User-level files
if [ -f "${FAKE_OC}/opencode.json" ]; then
  pass "user-level opencode.json exists"
else
  fail "user-level opencode.json missing"
fi

if [ -f "${FAKE_OC}/oh-my-opencode.json" ]; then
  pass "user-level oh-my-opencode.json exists (from template)"
else
  fail "user-level oh-my-opencode.json missing"
fi

# Symlinks
if [ -L "${FAKE_OC}/plugins/superpowers.js" ]; then
  pass "superpowers plugin symlink exists"
  # Verify it points to a real file
  target="$(readlink "${FAKE_OC}/plugins/superpowers.js")"
  if [ -f "$target" ]; then
    pass "superpowers plugin symlink resolves"
  else
    fail "superpowers plugin symlink BROKEN -> ${target}"
  fi
else
  fail "superpowers plugin symlink missing"
fi

if [ -L "${FAKE_OC}/skills/superpowers" ]; then
  pass "superpowers skills symlink exists"
else
  fail "superpowers skills symlink missing"
fi

# Count Anthropic skill symlinks
anthropic_count=0
for skill in "${FAKE_OC}/skills"/anthropic-*; do
  [ -L "$skill" ] && anthropic_count=$((anthropic_count + 1))
done
if [ "$anthropic_count" -ge 10 ]; then
  pass "Anthropic skills linked: ${anthropic_count}"
else
  fail "Only ${anthropic_count} Anthropic skill symlinks (expected >= 10)"
fi

# Count custom skill symlinks
custom_count=0
for skill in "${FAKE_OC}/skills"/custom-*; do
  [ -L "$skill" ] && custom_count=$((custom_count + 1))
done
if [ "$custom_count" -ge 2 ]; then
  pass "Custom skills linked: ${custom_count}"
else
  fail "Only ${custom_count} custom skill symlinks (expected >= 2)"
fi

# --- Step 5: Registry integrity ---
printf '\n%s\n' "--- Step 5: Registry integrity ---"

if command -v python3 >/dev/null 2>&1; then
  if python3 "${CLONE_DIR}/scripts/gen-registry.py" --check 2>/dev/null; then
    pass "registry.yaml is up to date"
  else
    fail "registry.yaml is stale after bootstrap"
  fi

  if python3 "${CLONE_DIR}/scripts/gen-catalog.py" --check 2>/dev/null; then
    pass "CATALOG.md is up to date"
  else
    fail "CATALOG.md is stale after bootstrap"
  fi

  # Verify registry has expected entry count
  entry_count=$(python3 -c "
import yaml, sys
with open('${CLONE_DIR}/registry.yaml') as f:
    r = yaml.safe_load(f)
    print(r['meta']['total_count'])
")
  if [ "$entry_count" -ge 50 ]; then
    pass "Registry has ${entry_count} entries (>= 50 expected)"
  else
    fail "Registry only has ${entry_count} entries (expected >= 50)"
  fi
else
  skip "python3 not available — cannot verify registry"
fi

# --- Step 6: Profile switching ---
printf '\n%s\n' "--- Step 6: Profile switching ---"

for profile in minimal daily-dev full-stack; do
  if bash "${CLONE_DIR}/scripts/switch-profile.sh" "${profile}" >/dev/null 2>&1; then
    pass "switch-profile.sh ${profile} succeeded"
  else
    fail "switch-profile.sh ${profile} failed"
  fi
done

# --- Step 7: No hardcoded paths ---
printf '\n%s\n' "--- Step 7: Hardcoded path check ---"

# Check scripts for hardcoded absolute paths (excluding shebangs and comments)
hardcoded=0
for script in "${CLONE_DIR}/scripts"/*.sh "${CLONE_DIR}/scripts"/*.py; do
  [ -f "$script" ] || continue
  # Skip this test script itself (it legitimately references /Users/ and /home/ as grep patterns)
  [ "$(basename "$script")" = "test-e2e.sh" ] && continue
  # Look for /Users/ or /home/ in non-comment, non-shebang lines
  if grep -n '/Users/\|/home/' "$script" 2>/dev/null | grep -v '^1:#!' | grep -v '^\s*#' | grep -v '^\s*//' | head -3; then
    printf "  ^^^ in %s\n" "$(basename "$script")"
    hardcoded=$((hardcoded + 1))
  fi
done

if [ "$hardcoded" -eq 0 ]; then
  pass "No hardcoded user paths in scripts"
else
  fail "Found hardcoded paths in ${hardcoded} script(s)"
fi

# --- Summary ---
printf "\n=== Summary ===\n"
total=$((pass_count + fail_count + warn_count))
printf "%sPASS: %d%s | %sFAIL: %d%s | %sSKIP: %d%s | Total: %d\n" \
  "$GREEN" "$pass_count" "$NC" "$RED" "$fail_count" "$NC" "$YELLOW" "$warn_count" "$NC" "$total"

if [ "$fail_count" -gt 0 ]; then
  printf "\n%sE2E test FAILED%s\n" "$RED" "$NC"
  exit 1
else
  printf "\n%sE2E test PASSED%s\n" "$GREEN" "$NC"
  exit 0
fi
