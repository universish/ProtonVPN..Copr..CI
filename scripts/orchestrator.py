#!/usr/bin/env python3
import os
import re
import sys
import json
import gzip
import shutil
import urllib.request
import subprocess

COPR_REPO = "universish/ProtonVPN..for..bye..DPI..and..Get..Lost..Fascism"
CHROOTS = [
    "fedora-44-x86_64",
    "fedora-rawhide-x86_64"
]

# Bağımlılık zinciri sırası
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
    os.remove(downloaded_path)
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

def print_copr_failure_log(build_id):
    """COPR API üzerinden Mock derleme hata günlüğünü ekrana yazar."""
    print(f"\n[!] Fetching remote Mock failure logs for Build {build_id}...")
    api_url = f"https://copr.fedorainfracloud.org/api_3/build/{build_id}"
    try:
        req = urllib.request.Request(api_url, headers={'User-Agent': 'ProtonVPN-CI'})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
        
        chroots_data = data.get("chroots", {})
        for chroot, chroot_info in chroots_data.items():
            if chroot_info.get("state") == "failed":
                result_url = chroot_info.get("result_url")
                if not result_url:
                    continue
                log_url = result_url.rstrip("/") + "/build.log.gz"
                print(f"\n--- [FAILED CHROOT: {chroot}] Log: {log_url} ---")
                try:
                    log_req = urllib.request.Request(log_url, headers={'User-Agent': 'ProtonVPN-CI'})
                    with urllib.request.urlopen(log_req) as log_resp:
                        decompressed = gzip.decompress(log_resp.read()).decode(errors='replace')
                        lines = decompressed.strip().split("\n")
                        print("\n".join(lines[-45:]))
                except Exception as log_err:
                    print(f"Could not read compressed log: {log_err}")
    except Exception as e:
        print(f"Could not contact COPR API for debug logs: {e}")

def submit_and_watch(srpm_path):
    cmd = ["copr-cli", "build", COPR_REPO, srpm_path, "--nowait"]
    for chroot in CHROOTS:
        cmd.extend(["-r", chroot])

    out = subprocess.check_output(cmd, text=True)
    match = re.search(r'Created builds:\s*([0-9]+)', out) or re.search(r'build/([0-9]+)', out) or re.search(r'([0-9]{6,})', out)
    if not match:
        return True
    build_id = match.group(1)
    print(f"[*] Watching build ID: {build_id} (Details: https://copr.fedorainfracloud.org/coprs/build/{build_id}/)...")
    res = subprocess.run(["copr-cli", "watch-build", build_id])
    if res.returncode != 0:
        print_copr_failure_log(build_id)
        return False
    return True

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

if __name__ == "__main__":
    main()
