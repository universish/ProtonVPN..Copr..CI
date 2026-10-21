<div align="center">

# 🛡️ Proton VPN for Fedora
### ⚡ Automated Downstream COPR Packaging CI/CD Pipeline ⚡

*Hermetic RPM Builds • Zero-Touch GNOME Integration • Active DPI Evasion*

<br/>

> *"Uncensored, reproducible, and cryptographically secure Proton VPN packaging for Fedora 44 & Rawhide."*

<br/>

<a href="https://github.com/universish/ProtonVPN..Copr..CI/actions">
  <img src="https://img.shields.io/github/actions/workflow/status/universish/ProtonVPN..Copr..CI/protonvpn-copr-ci.yml?style=flat-square&logo=githubactions&logoColor=white&label=CI%2FCD%20Builder" alt="CI/CD Status">
</a>
<a href="https://copr.fedorainfracloud.org/coprs/universish/ProtonVPN..for..bye..DPI..and..Get..Lost..Fascism/">
  <img src="https://img.shields.io/badge/Fedora%20COPR-Active%20Repo-51A2DA?style=flat-square&logo=fedora&logoColor=white" alt="Fedora COPR">
</a>
<a href="https://copr.fedorainfracloud.org/coprs/universish/ProtonVPN..for..bye..DPI..and..Get..Lost..Fascism/">
  <img src="https://img.shields.io/badge/Platform-Fedora%2044%20%7C%20Rawhide-294172?style=flat-square&logo=fedora&logoColor=white" alt="Platform">
</a>
<a href="https://copr.fedorainfracloud.org/coprs/universish/ProtonVPN..for..bye..DPI..and..Get..Lost..Fascism/">
  <img src="https://img.shields.io/badge/Arch-x86__64%20%7C%20aarch64-2d333b?style=flat-square&logo=linux&logoColor=white" alt="Architectures">
</a>
<a href="https://protonvpn.com/">
  <img src="https://img.shields.io/badge/Anti--DPI-Bypass%20Enforced-6d4aff?style=flat-square&logo=protonvpn&logoColor=white" alt="Anti-DPI">
</a>

</div>

---

---

Automated downstream RPM packaging pipeline for official Proton VPN desktop and CLI clients targeting **Fedora 44** and **Fedora Rawhide** on both **x86_64** and **aarch64 (ARM64)** architectures.

Designed to eliminate DPI blocks, enforce strict systemd-resolved DNS privacy, automatically resolve dependencies, and automatically enable the required GNOME Shell AppIndicator extension out of the box.

```text
  ____            _              __     ______  _   _ 
 |  _ \ _ __ ___ | |_ ___  _ __  \ \   / /  _ \| \ | |
 | |_) | '__/ _ \| __/ _ \| '_ \  \ \ / /| |_) |  \| |  [Fedora COPR CI]
 |  __/| | | (_) | || (_) | | | |  \ V / |  __/| |\  |  Autonomous Downstream
 |_|   |_|  \___/ \__\___/|_| |_|   \_/  |_|   |_| \_|  Packaging Engine
```

---

## Packaged Components & Dependency Tree

The repository automates the complete packaging chain from low-level authentication and routing libraries to the desktop GUI:

| Package | Type | Role |
| :--- | :--- | :--- |
| `protonvpn-stable-release` | Config | OpenPGP signing keys and local repository configuration |
| `python3-proton-core` | Core API | User authentication, session management, and FIDO2/2FA support |
| `python3-proton-keyring-linux` | Secrets | Hardware/desktop keyring integration (`gnome-keyring`, `libsecret`) |
| `python3-proton-vpn-network-manager` | Network | NetworkManager connection dispatcher and split-DNS controller |
| `python3-proton-vpn-local-agent` | Daemon/IPC | Modern IPC transport, wireguard tunnels, and traffic routing |
| `python3-proton-vpn-api-core` | Core VPN | VPN session orchestration, server list resolution, feature flags |
| `proton-vpn-daemon` | Service | Background system daemon with split-DNS leak protection |
| `proton-vpn-cli` | CLI Client | Standalone command-line client for headless and terminal usage |
| `proton-vpn-gtk-app` | GUI Client | Full GTK3 desktop interface |
| `proton-vpn-gnome-desktop` | Integration | GNOME AppIndicator tray auto-activation via GSchema override |

---

## Quick Installation

### 1. Enable the COPR Repository

Run the following command to enable this repository on your Fedora system:

```bash
sudo dnf copr enable -y universish/ProtonVPN..for..bye..DPI..and..Get..Lost..Fascism
```

> **Important (Avoiding Conflicts with Legacy Packages in the Official Fedora Repositories):**  
> Fedora’s default repositories contain very old versions of Proton (`0.3.3` and `0.36.6`). Set the repository priority so that the DNF package manager always prefers the latest COPR packages:
> ```bash
> sudo dnf config-manager addrepo --set-opts="copr:copr.fedorainfracloud.org:universish:ProtonVPN..for..bye..DPI..and..Get..Lost..Fascism.priority=10"
> ```

---

### 2. Install Proton VPN

#### 2.1. Complete Desktop Installation (GUI + CLI + Daemon):
```bash
sudo dnf install -y \
  proton-vpn-gnome-desktop \
  proton-vpn-gtk-app \
  proton-vpn-cli \
  proton-vpn-daemon \
  python3-proton-core \
  python3-proton-vpn-api-core \
  python3-proton-vpn-local-agent \
  python3-proton-vpn-network-manager \
  python3-proton-keyring-linux
```

#### 2.2. Headless / Server / CLI Only Installation:
```bash
sudo dnf install -y \
  proton-vpn-cli \
  proton-vpn-daemon \
  python3-proton-core \
  python3-proton-vpn-api-core \
  python3-proton-vpn-local-agent \
  python3-proton-vpn-network-manager \
  python3-proton-keyring-linux
```

---

### 3. Running & Managing the Service

#### 3.1. Start the Background Daemon:
```bash
sudo systemctl enable --now proton-vpn-daemon.service
```

#### 3.2. Launch the Graphical Application (GUI):
Launch it from your desktop application grid or via terminal:
```bash
protonvpn-app
```
*(On GNOME sessions, restart your session or log out once if the tray icon does not appear immediately after the first install).*

#### 3.3. Command Line Client (CLI):
Log in and connect:
```bash
protonvpn signin
protonvpn connect
```
Check status:
```bash
protonvpn status
```
Disconnect:
```bash
protonvpn disconnect
```

---

## Troubleshooting & Maintenance

### A. Package Conflict and “nothing provides libm.so.6” / Issue with Legacy Fedora Packages
If during installation, DNF attempts to fall back to older Fedora packages (`python3-proton-core-0.3.3` or `python3-proton-vpn-api-core-0.36.6`) or returns a conflict error:


1. Remove all installed old and incompatible Proton packages:
```bash
sudo dnf remove -y “proton-vpn*” “python3-proton*” “protonvpn*”
```
2. Completely clear and refresh the DNF cache:
```
sudo dnf clean all
sudo dnf makecache --refresh
```
3. Force installation directly from COPR, excluding Fedora’s legacy packages:
```
sudo dnf install -y \
  --disablerepo="fedora,updates" \
  --enablerepo="copr:copr.fedorainfracloud.org:universish:*" \
  proton-vpn-gnome-desktop \
  proton-vpn-gtk-app \
  proton-vpn-cli \
  proton-vpn-daemon \
  python3-proton-core \
  python3-proton-vpn-api-core \
  python3-proton-vpn-local-agent \
  python3-proton-vpn-network-manager \
  python3-proton-keyring-linux
```

### B. Upgrade & Refresh
When a new version is built in your COPR repository, to bypass the local cache and fetch the updates:
*  Update by refreshing the cache:
```bash
sudo dnf upgrade --refresh "proton-vpn*" "python3-proton*" "protonvpn*"
```

* If the cache gets stuck:
```bash
sudo dnf clean all
sudo dnf makecache --refresh
sudo dnf upgrade -y
```

### C. Uninstallation
To completely remove the application, its configurations, and the COPR repository from the system:

* Remove all packages:
```bash
sudo dnf remove -y "proton-vpn*" "python3-proton*" "protonvpn*"
```

* Disable the COPR repo:
```
sudo dnf copr disable -y universish/ProtonVPN..for..bye..DPI..and..Get..Lost..Fascism
```

---

# Target Platforms & Architectures

| Release | Architectures | Target Environments |
| :--- | :--- | :--- |
| **Fedora 44** | `x86_64`, `aarch64` | GNOME Desktop, KDE Plasma, CLI |
| **Fedora Rawhide** | `x86_64`, `aarch64` | GNOME Desktop, Generic, CLI |

---

## Technical Transparency & RPM-to-RPM Pipeline

This repository acts as an automated, transparent downstream packager. Rather than compiling untrusted third-party code from source or modifying Proton's core binaries, it ingests official upstream releases directly from Proton Technologies' repositories, enriches system-level integration hooks, and produces clean, native Fedora RPMs through Fedora's isolated COPR build environment.

---

### Pipeline Overview

```
[Official Proton Repository]
│
▼
1. Fetch Official RPM & Checksum Validation
│
▼
2. Ephemeral Inspection & Payload Extraction (rpm2cpio)
│
├─► Core Binary & Python Payloads Preserved (Untouched)
├─► Declarative Dependency Hardening (systemd-resolved, keyring)
└─► Native GNOME Integration (GSchema AppIndicator Override)
│
▼
3. Deterministic Source RPM (SRPM) Generation
│
▼
4. Hermetic Build in Fedora COPR Isolated Mock Chroot (F44 / Rawhide)
│
▼
[Signed Fedora COPR Binary RPMs]
```

---

### Detailed Transformation Steps

#### 1. Upstream Verification and Fetching
Every scheduled run directly monitors the official Proton repository (`repo.protonvpn.com/fedora-44-stable`). The pipeline pulls the official vendor RPMs:
- No arbitrary forks or unverified source mirrors are used.
- Upstream package versions and release metadata are strictly mirrored.

#### 2. Payload Extraction (`rpm2cpio` & `cpio`)
Inside an isolated container, the downloaded package is unpacked using standard POSIX tooling:

```bash
rpm2cpio proton-vpn-gnome-desktop-%{version}.%{_arch}.rpm | cpio -idmv
```

* **Zero Binary Tampering:** The application binaries, Python bytecode, cryptographic handling, WireGuard/OpenVPN integration, and authentication tokens are kept strictly unmodified. The core executable code remains byte-for-byte identical to Proton Technologies' official release.

#### 3. Integration & Dependency Hardening
* **DNS Leak Protection:** Adds an explicit `Requires: systemd-resolved` directive, ensuring Fedora's modern split-DNS architecture operates correctly with Proton's routing policies out of the box.
* **Credential Security:** Enforces `Requires: gnome-keyring` and `Requires: libsecret` to ensure secure hardware-backed or encrypted storage for user authentication tokens.
* **Network Infrastructure:** Links against `NetworkManager` and `NetworkManager-libnm` to prevent connection drops across desktop environments.
* **Out-of-the-Box GNOME AppIndicator Support:** Solves the common missing tray icon issue on GNOME by embedding a system-wide GSchema override:
```ini
[org.gnome.shell]
enabled-extensions=['appindicatorsupport@rgcjonas.gmail.com']
```
The `%post` and `%postun` scriptlets invoke `glib-compile-schemas` during package installation, instantly enabling tray visibility without requiring manual GNOME Extensions app tinkering.

#### 4. Clean SRPM Re-bundling & COPR Mock Isolation
* The enriched payload is wrapped into an RPM SPEC and packaged into a deterministic Source RPM (`.src.rpm`).
* The SRPM is dispatched to the **Fedora COPR build system**.
* COPR builds the final binary RPMs in clean, network-isolated mock chroots managed by the Fedora Infrastructure team.
* All build logs, environment variables, and build artifacts remain publicly inspectable and auditable.

---

### Security Guarantees
* **Auditable & Open-Source:** All packaging specs, fallback definitions, and build scripts are fully open source in this repository.
* **No Secret Injection / Backdoors:** CI runners never modify application logic, endpoints, or TLS verification routines.
* **Verifiable Builds:** You can inspect the exact SRPM and build log for every release directly on the [Fedora COPR Build History](https://www.google.com/search?q=https%3A%2F%2Fcopr.fedorainfracloud.org%2Fcoprs%2Funiversish%2FProtonVPN..for..bye..DPI..and..Get..Lost..Fascism%2Fbuilds%2F).

---

## Mission & Legal-Normative Basis

This project exists to guarantee unhindered access to open information, private communications, and secure network infrastructure in environments subject to arbitrary state censorship, pervasive surveillance, and digital authoritarianism.

### Human Rights & Legal Framework
Access to an uncensored internet and cryptographic privacy tools is a foundational prerequisite for exercising fundamental rights guaranteed under international law:
* **Article 19 of the Universal Declaration of Human Rights (UDHR):** *"Everyone has the right to freedom of opinion and expression; this right includes freedom to hold opinions without interference and to seek, receive and impart information and ideas through any media and regardless of frontiers."*
* **Article 17 of the International Covenant on Civil and Political Rights (ICCPR):** The protection of individuals against unlawful or arbitrary interference with privacy and correspondence.
* **UN General Assembly Resolution 68/167:** Reaffirming that the same rights individuals have offline must also be protected online, specifically privacy and freedom of expression.

### Threat Model: Deep Packet Inspection (DPI) & State Interference
Authoritarian governance frameworks and state-aligned telecommunications monopolies routinely weaponize:
* **Deep Packet Inspection (DPI):** Middleboxes analyzing Layer 7 payload headers, TLS ClientHello handshakes, and SNI (Server Name Indication) fields to throttle, tamper with, or outright sever independent communication channels.
* **DNS Hijacking & Cache Poisoning:** Forcing domestic recursive resolvers to redirect or block legitimate internet endpoints.
* **Administrative & Repository Blacklisting:** Restricting access to standard binary repositories, download mirrors, and official installation vectors to prevent citizens from obtaining cryptographic defense software.

### Operational Purpose
By maintaining an automated, continuous, and auditable downstream packaging pipeline on Fedora's official COPR infrastructure, this repository ensures that journalists, researchers, engineers, and everyday citizens under restrictive regimes can:
1. **Bootstrap Privacy Tools Seamlessly:** Deploy official Proton VPN clients and stealth-routing configurations via standard native package managers (`dnf`) without relying on blocked upstream landing pages.
2. **Prevent Routing & DNS Leakage:** Enforce strict split-DNS routing via native `systemd-resolved` integration, rendering ISP-level DNS manipulation ineffective.
3. **Sustain Digital Self-Defense:** Maintain reproducible access to authenticated, end-to-end encrypted tunnels designed to bypass DPI middleboxes and resist automated packet classification.

---

# License
* This packaging automation is provided under the [MIT License](https://www.google.com/search?q=https%3A%2F%2Fgithub.com%2Funiversish%2FProtonVPN..Copr..CI%2Fblob%2Fmain%2FLICENSE).
* Proton VPN software components retain their original upstream licenses (GPL-3.0-or-later).
