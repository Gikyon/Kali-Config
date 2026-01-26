#!/usr/bin/env bash
set -e

echo "[*] Kali-Config bootstrap starting..."

# ─── Root check ────────────────────────────────────────────────────────────────
if [[ $EUID -ne 0 ]]; then
  echo "[!] Run as root"
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "[*] Working directory: $ROOT_DIR"

# ─── Permissions ───────────────────────────────────────────────────────────────
chmod +x "$ROOT_DIR/setup-zsh.sh"
chmod +x "$ROOT_DIR/installer.py"

# ─── ZSH setup ────────────────────────────────────────────────────────────────
echo "[*] Running ZSH setup"
"$ROOT_DIR/zsh/setup-zsh.sh"

# ─── Tool installation ─────────────────────────────────────────────────────────
echo "[*] Running tool installer"
python3 "$ROOT_DIR/tools/installer.py"

echo "[✓] Bootstrap complete. Restart your terminal."
