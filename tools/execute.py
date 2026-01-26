#!/usr/bin/env python3

import subprocess
import shutil
import sys
from pathlib import Path

# ---------- Helpers ----------

def run_cmd(cmd: list[str], require_root: bool = False):
    """
    Run a shell command safely.
    """
    if require_root and shutil.which("sudo"):
        cmd = ["sudo"] + cmd

    print(f"[+] Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

def command_exists(cmd: str) -> bool:
    return shutil.which(cmd) is not None


# ---------- Install Methods ----------

def apt_install(packages: list[str]):
    """
    Install packages via apt.
    """
    if not packages:
        return
    try:
        print("[*] Installing via apt...")
        run_cmd(["apt", "update"], require_root=True)
        run_cmd(["apt", "install", "-y", *packages], require_root=True)
    except subprocess.CalledProcessError as e:
        print(f"[!] Error installing packages via apt: {e}")
        sys.exit(1)

def pipx_install(packages: list[str]):
    """
    Install Python CLI tools via pipx.
    """
    if not packages:
        return

    if not command_exists("pipx"):
        print("[!] pipx not found, installing...")
        run_cmd(["apt", "install", "-y", "pipx"], require_root=True)
        run_cmd(["pipx", "ensurepath"])

    print("[*] Installing via pipx...")
    for pkg in packages:
        run_cmd(["pipx", "install", pkg])

def git_clone(repos: dict[str, str]):
    """
    Clone GitHub repositories.

    repos = {
        "tool-name": "https://github.com/user/repo.git"
    }
    """
    base_path = Path("/opt")
    base_path.mkdir(parents=True, exist_ok=True)

    print(f"[*] Cloning repositories into {base_path}")

    for name, url in repos.items():
        dest = base_path / name

        if dest.exists():
            print(f"[=] Skipping {name}, already exists")
            continue

        run_cmd(["git", "clone", url, str(dest)])

def wget_download(files: dict[str, str], base_dir: str = "/opt"):
    """
    Download files using wget into their own directories.

    files = {
        "tool-name": "https://example.com/file"
    }
    """
    base_path = Path(base_dir)
    base_path.mkdir(parents=True, exist_ok=True)

    print(f"[*] Downloading files into {base_path}")

    for name, url in files.items():
        tool_dir = base_path / name
        tool_dir.mkdir(parents=True, exist_ok=True)

        filename = url.split("/")[-1]
        output_file = tool_dir / filename

        print(f"[+] Downloading {name} -> {output_file}")

        cmd = ["wget", "-O", str(output_file), url]
        run_cmd(cmd)

# ---------- more complex tools ----------

def install_vscode():
    """
    Install Visual Studio Code.
    """
    print("[*] Installing Visual Studio Code...")
    run_cmd(["wget", "-qO-", "https://packages.microsoft.com/keys/microsoft.asc", "|", "gpg", "--dearmor", ">", "/usr/share/keyrings/microsoft.gpg"], require_root=True)
    run_cmd(["sh", "-c", 'echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'], require_root=True)
    apt_install(["code"])