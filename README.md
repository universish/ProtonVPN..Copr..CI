# Proton VPN for Fedora (Automated COPR Packaging CI)

[![ProtonVPN Copr CI](https://github.com/universish/ProtonVPN..Copr..CI/actions/workflows/protonvpn-copr-ci.yml/badge.svg)](https://github.com/universish/ProtonVPN..Copr..CI/actions)

[COPR Build Status](https://copr.fedorainfracloud.org/coprs/universish/ProtonVPN..for..bye..DPI..and..Get..Lost..Fascism/)

Automated downstream RPM packaging pipeline for official Proton VPN desktop and CLI clients targeting **Fedora 44** and **Fedora Rawhide** on both **x86_64** and **aarch64 (ARM64)** architectures.

Designed to eliminate DPI blocks, enforce strict systemd-resolved DNS privacy, automatically resolve dependencies, and automatically enable the required GNOME Shell AppIndicator extension out of the box.

---

## Features

- **Native Package Identity:** Retains exact upstream package naming (`proton-vpn-gnome-desktop`, `protonvpn-stable-release`, `proton-vpn-cli`).
- **Fully Automated CI/CD:** Runs twice daily (before lunch and before end of workday, Swedish Time / CET/CEST).
- **Auto Version Bump & Sequential Release Tagging:** Automatically parses upstream repositories for new releases. If version `4.4.4` receives multiple builds, releases increment automatically (`4.4.4-1`, `4.4.4-2`).
- **Cascade Fallback Builds:** If a build fails against strict upstream spec files on COPR, the workflow automatically cascades through secondary and tertiary compatibility specs until a build succeeds.
- **Zero-Touch GNOME Integration:** Automatically pulls in and system-wide enables `gnome-shell-extension-appindicator` via a compiled GSchema override, so tray icons work immediately without manual user configuration.

---

## Quick Installation

### 1. Enable the COPR Repository

Run the following command to enable this repository:

```bash
sudo dnf copr enable universish/ProtonVPN..for..bye..DPI..and..Get..Lost..Fascism
```

### 2. Install Proton VPN

### 2.1. For GNOME and Desktop Environments (GUI):

```
sudo dnf install proton-vpn-gnome-desktop
```

Note: This automatically installs and configures `libappindicator-gtk3`, `gnome-shell-extension-appindicator`, `gnome-extensions-app`, `systemd-resolved` and `gnome-keyring`.

### 2.2. For Headless / Terminal Environments (CLI):

```
sudo dnf install proton-vpn-cli
```

**Note:** This automatically pulls in `NetworkManager` and `gnome-keyring` for headless credential management.

### 2.3. Running the Application

### 2.3.1. GUI Application:

Launch it from your desktop application grid or via terminal:

```
protonvpn-app
```

(On GNOME sessions, restart your session or log out once if the tray icon does not appear immediately after the first install).

### 2.3.2. CLI Application:

Log in to your account and connect:

```
protonvpn-cli login
protonvpn-cli connect
```

Check status:

```
protonvpn-cli status
```

### 2.4. Uninstallation

To completely remove Proton VPN, its configurations, and the repository release package:

```
sudo dnf remove proton-vpn-gnome-desktop protonvpn-stable-release
```

To remove the CLI tool:

```
sudo dnf remove proton-vpn-cli
```

To disable the COPR repository:

```
sudo dnf copr disable universish/ProtonVPN..for..bye..DPI..and..Get..Lost..Fascism
```

----

# Target Platforms & Architectures

| Release | Architectures | Target Environments |
| :--- | :--- | :--- |
| **Fedora 44** | `x86_64`, `aarch64` | GNOME Desktop, KDE Plasma, CLI |
| **Fedora Rawhide** | `x86_64`, `aarch64` | GNOME Desktop, Generic, CLI |

----

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

Upstream packages often assume manual user intervention or minimal desktop assumptions. This package bridges those gaps declaratively at the RPM specification level:

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
* **Verifiable Builds:** You can inspect the exact SRPM and build log for every release directly on the [Fedora COPR Build History](https://www.google.com/search?q=https://copr.fedorainfracloud.org/coprs/universish/ProtonVPN..for..bye..DPI..and..Get..Lost..Fascism/builds/).

----

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

----

# License
* This packaging automation is provided under the [MIT License](https://github.com/universish/ProtonVPN..Copr..CI/blob/main/LICENSE).
* Proton VPN software components retain their original upstream licenses (GPL-3.0-or-later).
