%global debug_package %{nil}
%global _python_bytecompile_extra 0

Name:           proton-vpn-gnome-desktop
Version:        0.11.0
Release:        1%{?dist}
Summary:        Proton VPN Linux Desktop application (Compatibility Fallback Build)
License:        GPL-3.0-or-later
URL:            https://protonvpn.com/
BuildArch:      noarch

Source0:        proton-vpn-gnome-desktop-upstream.rpm

BuildRequires:  cpio
BuildRequires:  rpm-build

Requires:       gnome-keyring
Requires:       systemd-resolved
Requires:       NetworkManager
Recommends:     libappindicator-gtk3
Recommends:     gnome-shell-extension-appindicator

%description
Proton VPN Desktop client repackaged with relaxed dependency requirements.

%prep
%setup -c -T

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
cd %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idmv || :

mkdir -p %{buildroot}%{_docdir}/%{name}
echo "Repackaged by universish ProtonVPN Copr CI (Compat)" > %{buildroot}%{_docdir}/%{name}/README.copr

cd %{_builddir}/%{name}-%{version}
find %{buildroot} -type f -o -type l | sed "s|^%{buildroot}||" > files.list

%files -f files.list

%changelog
* Tue Oct 06 2026 Saffet Yavuz <universish@github> - 0.11.0-1
- Compat build.
