%global debug_package %{nil}
%global _python_bytecompile_extra 0

Name:           proton-vpn-gtk-app
Version:        0.5.2
Release:        1%{?dist}
Summary:        Proton VPN GTK Graphical Application
License:        GPL-3.0-or-later
URL:            https://protonvpn.com/
BuildArch:      noarch

Source0:        proton-vpn-gtk-app-upstream.rpm

BuildRequires:  cpio
BuildRequires:  rpm-build

Requires:       proton-vpn-daemon
Requires:       python3-gobject
Requires:       gtk3
Requires:       libsecret

%description
Graphical user interface application for Proton VPN based on GTK.

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
* Tue Oct 06 2026 Saffet Yavuz <universish@github> - 0.5.2-1
- Initial GTK GUI application packaging.
