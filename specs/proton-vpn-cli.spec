Name:           proton-vpn-cli
Version:        4.4.4
Release:        1%{?dist}
Summary:        Proton VPN Command Line Interface
License:        GPL-3.0-or-later
URL:            https://protonvpn.com/
ExclusiveArch:  x86_64 aarch64

Source0:        https://repo.protonvpn.com/fedora-44-stable/protonvpn-stable-release/proton-vpn-cli-%{version}.%{_arch}.rpm

BuildRequires:  cpio
BuildRequires:  rpm-build

Requires:       gnome-keyring
Requires:       NetworkManager
Requires:       python3
Requires:       libsecret

%description
Proton VPN official CLI client rebuilt for Fedora environments.

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
- Automated CLI packaging.
