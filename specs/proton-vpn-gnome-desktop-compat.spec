Name:           proton-vpn-gnome-desktop
Version:        4.4.4
Release:        1%{?dist}
Summary:        Proton VPN Linux Desktop application (Compatibility Fallback Build)
License:        GPL-3.0-or-later
URL:            https://protonvpn.com/
ExclusiveArch:  x86_64 aarch64

Source0:        https://repo.protonvpn.com/fedora-44-stable/protonvpn-stable-release/proton-vpn-gnome-desktop-%{version}.%{_arch}.rpm

BuildRequires:  cpio
BuildRequires:  rpm-build

Requires:       gnome-keyring
Requires:       systemd-resolved
Requires:       NetworkManager
Recommends:     libappindicator-gtk3
Recommends:     gnome-shell-extension-appindicator
Recommends:     gnome-extensions-app

%description
Proton VPN Desktop client repackaged with relaxed dependency requirements
for extended Fedora Rawhide and secondary environment compatibility.

%prep
%setup -c -T

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
cd %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idmv

%files
/*

%changelog
* Tue Oct 06 2026 Saffet Yavuz <universish@github> - 4.4.4-1
- Fallback packaging with recommended dependencies.
