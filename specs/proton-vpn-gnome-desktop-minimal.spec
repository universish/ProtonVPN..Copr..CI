%global debug_package %{nil}

Name:           proton-vpn-gnome-desktop
Version:        0.11.0
Release:        1%{?dist}
Summary:        Proton VPN Linux Desktop application (Minimal Core Payload)
License:        GPL-3.0-or-later
URL:            https://protonvpn.com/
ExclusiveArch:  x86_64 aarch64 noarch

Source0:        proton-vpn-gnome-desktop-upstream.rpm

BuildRequires:  cpio
BuildRequires:  rpm-build

Requires:       NetworkManager

%description
Proton VPN Desktop core package.

%prep
%setup -c -T

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
cd %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idmv || :
find %{buildroot} -not -type d | sed "s|^%{buildroot}||" > %{_builddir}/files.list

%files -f %{_builddir}/files.list

%changelog
* Tue Oct 06 2026 Saffet Yavuz <universish@github> - 0.11.0-1
- Minimal packaging.
