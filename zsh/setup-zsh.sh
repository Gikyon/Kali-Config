#!/bin/sh
set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
ZSHRC_SOURCE="$REPO_DIR/zsh/zshrc"

echo "[*] Starting system-wide zsh configuration..."

setup_user() {
  USERNAME="$1"
  USER_HOME="$2"

  echo "[*] Configuring zsh for: $USERNAME ($USER_HOME)"

  USER_ZSH="$USER_HOME/.oh-my-zsh"
  USER_CUSTOM="$USER_ZSH/custom"

  # -------------------------
  # Install Oh My Zsh
  # -------------------------
  if [ ! -d "$USER_ZSH" ]; then
    echo "  └─ Installing Oh My Zsh"
    if [ "$USERNAME" = "root" ]; then
      RUNZSH=no CHSH=no sh -c \
        "curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh"
    else
      sudo -u "$USERNAME" env RUNZSH=no CHSH=no sh -c \
        "curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh"
    fi
  else
    echo "  └─ Oh My Zsh already installed"
  fi

  # -------------------------
  # Plugins
  # -------------------------
  mkdir -p "$USER_CUSTOM/plugins"

  [ -d "$USER_CUSTOM/plugins/zsh-autosuggestions" ] || \
    git clone https://github.com/zsh-users/zsh-autosuggestions \
      "$USER_CUSTOM/plugins/zsh-autosuggestions"

  [ -d "$USER_CUSTOM/plugins/zsh-syntax-highlighting" ] || \
    git clone https://github.com/zsh-users/zsh-syntax-highlighting \
      "$USER_CUSTOM/plugins/zsh-syntax-highlighting"

  # -------------------------
  # zshrc
  # -------------------------
  cp "$ZSHRC_SOURCE" "$USER_HOME/.zshrc"

  # -------------------------
  # Ownership
  # -------------------------
  chown -R "$USERNAME:$USERNAME" "$USER_HOME/.oh-my-zsh" "$USER_HOME/.zshrc"

  echo "  └─ Done"
}

# -------------------------
# Normal users
# -------------------------
for USER_HOME in /home/*; do
  [ -d "$USER_HOME" ] || continue
  USERNAME="$(basename "$USER_HOME")"
  id "$USERNAME" >/dev/null 2>&1 || continue
  setup_user "$USERNAME" "$USER_HOME"
done

# -------------------------
# Root
# -------------------------
setup_user "root" "/root"

echo "[✔] Zsh configured for all users (including root)"
echo "Log out and back in, or run: zsh"
