#!/bin/sh

set -e

echo "[*] Installing Oh My Zsh..."

# Install Oh My Zsh if not already installed
if [ ! -d "$HOME/.oh-my-zsh" ]; then
  RUNZSH=no CHSH=no sh -c     "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
else
  echo "[*] Oh My Zsh already installed"
fi

ZSH_CUSTOM="${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}"

echo "[*] Installing zsh plugins..."

# zsh-autosuggestions
if [ ! -d "$ZSH_CUSTOM/plugins/zsh-autosuggestions" ]; then
  git clone https://github.com/zsh-users/zsh-autosuggestions     "$ZSH_CUSTOM/plugins/zsh-autosuggestions"
else
  echo "[*] zsh-autosuggestions already installed"
fi

# zsh-syntax-highlighting
if [ ! -d "$ZSH_CUSTOM/plugins/zsh-syntax-highlighting" ]; then
  git clone https://github.com/zsh-users/zsh-syntax-highlighting     "$ZSH_CUSTOM/plugins/zsh-syntax-highlighting"
else
  echo "[*] zsh-syntax-highlighting already installed"
fi

echo "[*] Ensuring .zshrc exists..."

# Create .zshrc if missing
if [ ! -f "$HOME/.zshrc" ]; then
  cp "$HOME/.oh-my-zsh/templates/zshrc.zsh-template" "$HOME/.zshrc"
fi

echo "[*] Zsh setup complete!"

echo "[*] Reloading zsh config..."
if [ -n "$ZSH_VERSION" ]; then
  . "$HOME/.zshrc"
else
  echo "[*] Restart your terminal or run: zsh"
fi

echo "[*] moving zshrc file."
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp "$ROOT_DIR/zsh/setup-zsh.sh" "$HOME/.zshrc"