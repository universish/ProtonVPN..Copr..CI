# ProtonVPN..Copr..CI

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

# License
* This packaging automation is provided under the [MIT License](https://github.com/universish/ProtonVPN..Copr..CI/blob/main/LICENSE).
* Proton VPN software components retain their original upstream licenses (GPL-3.0-or-later).
