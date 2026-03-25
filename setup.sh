#!/usr/bin/env bash
set -euo pipefail

install_claude_code() {
  curl -fsSL https://claude.ai/install.sh | bash
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
  install_claude_code
  configure_path
  write_claude_md
  echo "Setup complete. Run 'source ~/.zshrc' or open a new terminal."
}

main
