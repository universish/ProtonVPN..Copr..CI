Name:           proton-vpn-gnome-desktop
Version:        4.4.4
Release:        1%{?dist}
Summary:        Proton VPN Linux Desktop application (Minimal Core Payload)
License:        GPL-3.0-or-later
URL:            https://protonvpn.com/
ExclusiveArch:  x86_64 aarch64

Source0:        proton-vpn-gnome-desktop-upstream.rpm

BuildRequires:  cpio
BuildRequires:  rpm-build

Requires:       NetworkManager

%description
Proton VPN Desktop core package without optional desktop hooks.

%prep
%setup -c -T

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
cd %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idmv

%files
/*
