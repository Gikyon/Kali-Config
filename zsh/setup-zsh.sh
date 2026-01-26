#!/bin/sh
set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
ZSHRC_SOURCE="$REPO_DIR/zshrc"

echo "[*] Starting system-wide zsh configuration..."

setup_user() {
  USERNAME="$1"
  USER_HOME="$2"

  echo "[*] Configuring zsh for: $USERNAME ($USER_HOME)"

  USER_ZSH="$USER_HOME/.oh-my-zsh"
  USER_CUSTOM="$USER_ZSH/custom"

  # -------------------------
  # Install Oh My Zsh (verify real install)
  # -------------------------
  if [ ! -f "$USER_ZSH/oh-my-zsh.sh" ]; then
    echo "  └─ Installing Oh My Zsh"

    # Clean broken install if present
    rm -rf "$USER_ZSH"

    if [ "$USERNAME" = "root" ]; then
      RUNZSH=no CHSH=no sh -c \
        "curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh | sh"
    else
      sudo -u "$USERNAME" env RUNZSH=no CHSH=no sh -c \
        "curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh | sh"
    fi
  else
    echo "  └─ Oh My Zsh already installed"
  fi

  # -------------------------
  # Plugins (install as user)
  # -------------------------
  if [ "$USERNAME" = "root" ]; then
    mkdir -p "$USER_CUSTOM/plugins"

    [ -d "$USER_CUSTOM/plugins/zsh-autosuggestions" ] || \
      git clone https://github.com/zsh-users/zsh-autosuggestions \
        "$USER_CUSTOM/plugins/zsh-autosuggestions"

    [ -d "$USER_CUSTOM/plugins/zsh-syntax-highlighting" ] || \
      git clone https://github.com/zsh-users/zsh-syntax-highlighting \
        "$USER_CUSTOM/plugins/zsh-syntax-highlighting"
  else
    sudo -u "$USERNAME" mkdir -p "$USER_CUSTOM/plugins"

    sudo -u "$USERNAME" sh -c '
      [ -d "'"$USER_CUSTOM/plugins/zsh-autosuggestions"'" ] || \
        git clone https://github.com/zsh-users/zsh-autosuggestions \
          "'"$USER_CUSTOM/plugins/zsh-autosuggestions"'"
    '

    sudo -u "$USERNAME" sh -c '
      [ -d "'"$USER_CUSTOM/plugins/zsh-syntax-highlighting"'" ] || \
        git clone https://github.com/zsh-users/zsh-syntax-highlighting \
          "'"$USER_CUSTOM/plugins/zsh-syntax-highlighting"'"
    '
  fi

  # -------------------------
  # zshrc
  # -------------------------
  cp "$ZSHRC_SOURCE" "$USER_HOME/.zshrc"

  # -------------------------
  # Ownership (non-root only)
  # -------------------------
  if [ "$USERNAME" != "root" ]; then
    chown -R "$USERNAME:$USERNAME" \
      "$USER_HOME/.oh-my-zsh" \
      "$USER_HOME/.zshrc"
  fi

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
