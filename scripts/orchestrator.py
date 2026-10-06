#!/usr/bin/env python3
import os
import re
import sys
import shutil
import subprocess

COPR_REPO = "universish/ProtonVPN..for..bye..DPI..and..Get..Lost..Fascism"
CHROOTS = [
    "fedora-44-x86_64",
    "fedora-rawhide-x86_64"
]

PACKAGES_TO_PROCESS = [
    ("protonvpn-stable-release", "specs/protonvpn-stable-release.spec"),
    ("proton-vpn-daemon", "specs/proton-vpn-daemon.spec"),
    ("proton-vpn-cli", "specs/proton-vpn-cli.spec"),
    ("proton-vpn-gtk-app", "specs/proton-vpn-gtk-app.spec"),
    ("proton-vpn-gnome-desktop", "specs/proton-vpn-gnome-desktop.spec")
]

def setup_upstream_repo():
    repo_content = """[protonvpn-fedora-stable]
name=ProtonVPN Fedora Stable
baseurl=https://repo.protonvpn.com/fedora-$releasever-stable/
        https://repo.protonvpn.com/fedora-44-stable/
        https://repo.protonvpn.com/fedora-42-stable/
enabled=1
gpgcheck=0
repo_gpgcheck=0
"""
    os.makedirs("/etc/yum.repos.d", exist_ok=True)
    with open("/etc/yum.repos.d/protonvpn.repo", "w") as f:
        f.write(repo_content)
    print("[*] Proton upstream repo active on runner.")

def fetch_package(pkg_name):
    print(f"\n[*] Fetching upstream RPM: {pkg_name}...")
    subprocess.check_call(["dnf", "download", "--refresh", "--destdir=specs", pkg_name])

    downloaded = [
        f for f in os.listdir("specs")
        if f.startswith(pkg_name) and f.endswith(".rpm") and not f.endswith("-upstream.rpm")
    ]
    if not downloaded:
        raise RuntimeError(f"Could not find downloaded RPM for {pkg_name}")

    downloaded_path = os.path.join("specs", downloaded[0])
    version = subprocess.check_output(
        ["rpm", "-qp", "--qf", "%{VERSION}", downloaded_path], text=True
    ).strip()

    target_upstream = os.path.join("specs", f"{pkg_name}-upstream.rpm")
    shutil.copyfile(downloaded_path, target_upstream)
    os.remove(downloaded_path)  # Geçici indirilen dosyayı sil
    print(f"[+] Ingested {pkg_name} version: {version}")
    return version

def update_spec(spec_path, version):
    if not os.path.exists(spec_path):
        return
    with open(spec_path, "r") as f:
        content = f.read()
    content = re.sub(r'^(Version:\s*).*$', rf'\g<1>{version}', content, flags=re.MULTILINE)
    with open(spec_path, "w") as f:
        f.write(content)

def build_srpm(spec_file):
    os.makedirs("build_srpm", exist_ok=True)
    shutil.rmtree("build_srpm/SRPMS", ignore_errors=True)
    cmd = [
        "rpmbuild",
        "-bs",
        "--define", f"_topdir {os.path.abspath('build_srpm')}",
        "--define", f"_sourcedir {os.path.abspath('specs')}",
        spec_file
    ]
    subprocess.check_call(cmd)
    srpms = [os.path.join("build_srpm/SRPMS", f) for f in os.listdir("build_srpm/SRPMS") if f.endswith(".src.rpm")]
    return srpms[0]
            
def submit_and_watch(srpm_path):
    cmd = ["copr-cli", "build", COPR_REPO, srpm_path, "--nowait"]
    for chroot in CHROOTS:
        cmd.extend(["-r", chroot])

    out = subprocess.check_output(cmd, text=True)
    match = re.search(r'Created builds:\s*([0-9]+)', out) or re.search(r'build/([0-9]+)', out) or re.search(r'([0-9]{6,})', out)
    build_id = match.group(1)
    print(f"[*] Watching build ID: {build_id}...")
    res = subprocess.run(["copr-cli", "watch-build", build_id])
    return res.returncode == 0

def main():
    setup_upstream_repo()
    os.makedirs("specs", exist_ok=True)

    for pkg_name, spec_file in PACKAGES_TO_PROCESS:
        if not os.path.exists(spec_file):
            print(f"[!] Warning: {spec_file} does not exist. Skipping.")
            continue

        try:
            version = fetch_package(pkg_name)
            update_spec(spec_file, version)
            srpm = build_srpm(spec_file)
            print(f"[*] Submitting {pkg_name} ({version}) to COPR...")
            if not submit_and_watch(srpm):
                print(f"[ERROR] Build failed for {pkg_name}!")
                sys.exit(1)
            print(f"[SUCCESS] {pkg_name} successfully built and signed on COPR!")
        except Exception as e:
            print(f"[CRITICAL] Error handling {pkg_name}: {e}")
            sys.exit(1)
# Eğer spec içinde Source0 tanımlı değilse indirme yapmadan direkt SRPM üret
        if pkg_name == "protonvpn-stable-release":
            srpm = build_srpm(spec_file)
        else:
            version = fetch_package(pkg_name)
            update_spec(spec_file, version)
            srpm = build_srpm(spec_file)
if __name__ == "__main__":
    main()
