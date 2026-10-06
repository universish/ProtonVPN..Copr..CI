#!/usr/bin/env python3
import os
import re
import sys
import shutil
import subprocess

COPR_REPO = "universish/ProtonVPN..for..bye..DPI..and..Get..Lost..Fascism"
CHROOTS = [
    "fedora-44-x86_64",
    "fedora-44-aarch64",
    "fedora-rawhide-x86_64",
    "fedora-rawhide-aarch64"
]

SPEC_CANDIDATES = [
    "specs/proton-vpn-gnome-desktop.spec",
    "specs/proton-vpn-gnome-desktop-compat.spec",
    "specs/proton-vpn-gnome-desktop-minimal.spec"
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
    print("[*] Proton upstream repository configured.")

def fetch_upstream_rpm(pkg_name="proton-vpn-gnome-desktop"):
    setup_upstream_repo()
    os.makedirs("specs", exist_ok=True)

    print(f"[*] Downloading latest upstream package: {pkg_name}...")
    subprocess.check_call(["dnf", "download", "--refresh", "--destdir=specs", pkg_name])

    downloaded = [
        f for f in os.listdir("specs")
        if f.startswith(pkg_name) and f.endswith(".rpm") and not f.endswith("-upstream.rpm")
    ]
    if not downloaded:
        raise RuntimeError(f"Could not find downloaded RPM for {pkg_name} in specs/")

    downloaded_path = os.path.join("specs", downloaded[0])
    version = subprocess.check_output(
        ["rpm", "-qp", "--qf", "%{VERSION}", downloaded_path], text=True
    ).strip()

    target_upstream = os.path.join("specs", f"{pkg_name}-upstream.rpm")
    shutil.copyfile(downloaded_path, target_upstream)
    print(f"[+] Downloaded: {downloaded[0]} (Version: {version}) -> Ready as {target_upstream}")
    return version

def get_tracking_state():
    default_version = "0.0.0"
    default_release = 0

    if not os.path.exists("VERSION"):
        with open("VERSION", "w") as f:
            f.write(default_version)
    if not os.path.exists("RELEASE_NUM"):
        with open("RELEASE_NUM", "w") as f:
            f.write(str(default_release))

    with open("VERSION", "r") as f:
        v = f.read().strip()
    with open("RELEASE_NUM", "r") as f:
        try:
            r = int(f.read().strip())
        except ValueError:
            r = default_release

    return v, r

def update_spec_file(filepath, new_version, new_release):
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r') as f:
        content = f.read()

    content = re.sub(r'^(Version:\s*).*$', rf'\g<1>{new_version}', content, flags=re.MULTILINE)
    content = re.sub(r'^(Release:\s*)[0-9]+', rf'\g<1>{new_release}', content, flags=re.MULTILINE)

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"[*] Updated {filepath} -> Version: {new_version}, Release: {new_release}")

def build_srpm(spec_file):
    os.makedirs("build_srpm", exist_ok=True)
    cmd = [
        "rpmbuild",
        "-bs",
        "--define", f"_topdir {os.path.abspath('build_srpm')}",
        "--define", f"_sourcedir {os.path.abspath('specs')}",
        spec_file
    ]
    subprocess.check_call(cmd)
    srpms = [os.path.join("build_srpm/SRPMS", f) for f in os.listdir("build_srpm/SRPMS") if f.endswith(".src.rpm")]
    if not srpms:
        raise RuntimeError("No SRPM generated!")
    return srpms[0]

def submit_and_watch_copr(srpm_path):
    cmd = ["copr-cli", "build", COPR_REPO, srpm_path, "--nowait"]
    for chroot in CHROOTS:
        cmd.extend(["-r", chroot])

    out = subprocess.check_output(cmd, text=True)
    print(f"[+] COPR Build submitted:\n{out}")

    match = re.search(r'Created builds:\s*([0-9]+)', out) or re.search(r'build/([0-9]+)', out) or re.search(r'([0-9]{6,})', out)
    if not match:
        return True

    build_id = match.group(1)
    print(f"[*] Watching COPR build ID: {build_id} (Details: https://copr.fedorainfracloud.org/coprs/build/{build_id}/)...")
    result = subprocess.run(["copr-cli", "watch-build", build_id])

    if result.returncode != 0:
        print(f"\n[!] Build {build_id} failed. Check detailed mock logs at:")
        print(f"    https://copr.fedorainfracloud.org/coprs/build/{build_id}/\n")
        return False
    return True

def main():
    tracked_version, tracked_release = get_tracking_state()
    upstream_version = fetch_upstream_rpm("proton-vpn-gnome-desktop")

    if upstream_version != tracked_version:
        print(f"[*] New upstream version detected: {upstream_version} (tracked: {tracked_version})")
        target_version = upstream_version
        target_release = 1
    else:
        print(f"[*] Upstream version unchanged ({tracked_version}). Incrementing build sequence.")
        target_version = tracked_version
        target_release = tracked_release + 1

    build_success = False
    for spec_file in SPEC_CANDIDATES:
        if not os.path.exists(spec_file):
            continue
        print(f"\n[===] Attempting build with SPEC: {spec_file} [===]")
        update_spec_file(spec_file, target_version, target_release)
        
        try:
            srpm = build_srpm(spec_file)
            success = submit_and_watch_copr(srpm)
            if success:
                print(f"[SUCCESS] Build passed using {spec_file}!")
                build_success = True
                break
            else:
                print(f"[FAIL] COPR build failed with {spec_file}. Cascading to fallback spec...")
        except Exception as e:
            print(f"[ERROR] Build failed for {spec_file}: {e}")

    if build_success:
        with open("VERSION", "w") as f:
            f.write(target_version)
        with open("RELEASE_NUM", "w") as f:
            f.write(str(target_release))
        sys.exit(0)
    else:
        print("[CRITICAL] All candidate SPEC builds failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
