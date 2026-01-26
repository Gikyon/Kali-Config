import execute

# ---------- Example Usage ----------
# need to add :
# potatoes
# enable all privs
# common exploits
# vscode


def main():
    apt_packages = [
        "impacket",
        "bloodhound",
        "pspy",
        "cewl",
        "seclists",
        "docker.io",
        "rlwrap",
        "pipx"
#        "keepassxc",
#        "code"
    ]

    pipx_packages = [
        "git-dumper",
        "uploadserver",
        "penelope",
        "bloodyAD"
    ]

    git_repos = {
        "rusthound": "https://github.com/NH-RED-TEAM/RustHound.git",
        "runascs": "https://github.com/antonioCoco/RunasCs.git",
        "chisel": "https://github.com/jpillora/chisel.git",
        "ligolo": "https://github.com/nicocha30/ligolo-ng.git",
        "username-anarchy": "https://github.com/urbanadventurer/username-anarchy.git",
        "shcheck": "https://github.com/santoru/shcheck.git",
        "Graph-Runner": "https://github.com/dafthack/GraphRunner.git",
        "pygpoabuse" : "https://github.com/Hackndo/pyGPOAbuse.git",
        "pkinit" : "https://github.com/dirkjanm/PKINITtools.git",
        "ghostpack" : "https://github.com/r3motecontrol/Ghostpack-CompiledBinaries.git",
        "pywhisker" : "https://github.com/ShutdownRepo/pywhisker.git",
        "pth-toolkit" : "https://github.com/byt3bl33d3r/pth-toolkit.git",
        "wp-rce" : "https://github.com/p0dalirius/Wordpress-webshell-plugin.git",
        "impacket" : "https://github.com/fortra/impacket.git"
    }

    wget_files = {
        "pspy64": "https://github.com/DominicBreuker/pspy/releases/download/v1.2.1/pspy64"
    }

    execute.apt_install(apt_packages)
    execute.pipx_install(pipx_packages)
    execute.git_clone(git_repos)
    execute.wget_download(wget_files)


if __name__ == "__main__":
    main()
