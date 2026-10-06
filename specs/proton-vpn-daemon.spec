%global debug_package %{nil}
%global _python_bytecompile_extra 0

Name:           proton-vpn-daemon
Version:        0.13.8
Release:        1%{?dist}
Summary:        Proton VPN Core Daemon Service
License:        GPL-3.0-or-later
URL:            https://protonvpn.com/
BuildArch:      noarch

Source0:        proton-vpn-daemon-upstream.rpm

BuildRequires:  cpio
BuildRequires:  rpm-build

Requires:       python3
Requires:       NetworkManager
Requires:       systemd-resolved
Requires:       gnome-keyring

%description
Core background daemon managing VPN connections, WireGuard tunnels, and routing.

%prep
%setup -c -T

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
cd %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idmv || :

mkdir -p %{buildroot}%{_docdir}/%{name}
echo "Repackaged by universish ProtonVPN Copr CI" > %{buildroot}%{_docdir}/%{name}/README.copr

cd %{_builddir}/%{name}-%{version}
find %{buildroot} -type f -o -type l | sed "s|^%{buildroot}||" > files.list

%files -f files.list

%changelog
* Tue Oct 06 2026 Saffet Yavuz <universish@github> - 0.13.8-1
- Initial daemon packaging.
