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
    Install Python CLI tools via pipx for all users (including root).
    """
    if not packages:
        return

    # Ensure pipx exists system-wide
    if not command_exists("pipx"):
        print("[!] pipx not found, installing...")
        run_cmd(["apt", "install", "-y", "pipx"], require_root=True)

    users = []

    # Normal users
    for home in Path("/home").iterdir():
        if home.is_dir():
            users.append((home.name, home))

    # Root
    users.append(("root", Path("/root")))

    print("[*] Installing pipx packages for all users...")

    for username, home in users:
        print(f"  └─ User: {username}")

        env = {
            "HOME": str(home),
            "PIPX_HOME": f"{home}/.local/share/pipx",
            "PIPX_BIN_DIR": f"{home}/.local/bin",
            "PATH": f"{home}/.local/bin:/usr/bin:/bin",
        }

        # Ensure directories exist
        run_cmd(
            ["mkdir", "-p", env["PIPX_HOME"], env["PIPX_BIN_DIR"]],
            require_root=True,
        )

        # Ensure path is registered
        run_cmd(
            ["pipx", "ensurepath"],
            require_root=(username == "root"),
        )

        for pkg in packages:
            if username == "root":
                run_cmd(["pipx", "install", "--force", pkg])
            else:
                run_cmd(
                    ["sudo", "-u", username, "pipx", "install", "--force", pkg]
                )

    print("[+] pipx packages installed for all users")


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

    vscode_dir = "/opt/vscode"
    vscode_deb = f"{vscode_dir}/vscode.deb"

    run_cmd(["mkdir", "-p", vscode_dir], require_root=True)

    run_cmd([
        "wget",
        "-O",
        vscode_deb,
        "https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64"
    ], require_root=True)

    # Install the .deb properly
    run_cmd(["apt", "install", "-y", f"{vscode_deb}"], require_root=True)

    # Fix any missing deps just in case
    run_cmd(["apt", "-f", "install", "-y"], require_root=True)

    print("[+] Visual Studio Code installed")

