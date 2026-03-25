#!/usr/bin/env bash
set -euo pipefail

SPINNER_FRAMES=(⠋ ⠙ ⠹ ⠸ ⠼ ⠴ ⠦ ⠧ ⠇ ⠏)
SPINNER_PID=""

start_spinner() {
  local msg="$1"
  (
    i=0
    while true; do
      printf "\r${SPINNER_FRAMES[$((i % ${#SPINNER_FRAMES[@]}))]} %s" "$msg"
      i=$((i + 1))
      sleep 0.08
    done
  ) &
  SPINNER_PID=$!
}

stop_spinner() {
  local status=$1 msg="$2"
  kill "$SPINNER_PID" 2>/dev/null
  wait "$SPINNER_PID" 2>/dev/null || true
  SPINNER_PID=""
  if [ "$status" -eq 0 ]; then
    printf "\r✓ %s\n" "$msg"
  else
    printf "\r✗ %s\n" "$msg"
  fi
}

run_step() {
  local label="$1" success_msg="$2" fail_msg="$3"
  shift 3
  start_spinner "$label"
  local err
  err=$("$@" 2>&1) && rc=0 || rc=$?
  stop_spinner $rc "$([ $rc -eq 0 ] && echo "$success_msg" || echo "$fail_msg")"
  if [ $rc -ne 0 ]; then
    printf "  Error: %s\n" "$err"
    exit 1
  fi
}

install_claude_code() {
  curl -fsSL https://claude.ai/install.sh | bash > /dev/null 2>&1
}

configure_path() {
  local entry='export PATH="$HOME/.local/bin:$PATH"'
  if ! grep -qF '.local/bin' ~/.zshrc 2>/dev/null; then
    echo "$entry" >> ~/.zshrc
  fi
}

write_claude_md() {
  mkdir -p ~/.claude
  cat > ~/.claude/CLAUDE.md << 'CONTENT'
- In all interactions and commit messages, be extremely concise and sacrifice grammer for the sake of concision.

## Plans

- At the end of each plan, give me a list of unresolved questions to answer, if any. Make the questions extremely concise. Sacrifice grammer for the sake of concision.
- Make the plan multi-phase after all the unresolved questions are resolved.
CONTENT
}

main() {
  run_step "Installing Claude Code..." "Claude Code installed" "Claude Code install failed" install_claude_code
  run_step "Configuring PATH..." "PATH configured" "PATH config failed" configure_path
  run_step "Writing CLAUDE.md..." "CLAUDE.md written" "CLAUDE.md write failed" write_claude_md
  echo ""
  echo "Setup complete. Run 'source ~/.zshrc' or open a new terminal."
}

main
