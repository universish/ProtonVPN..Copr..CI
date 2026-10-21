%global debug_package %{nil}
%global __brp_python_bytecompile %{nil}
%global __brp_mangle_shebangs %{nil}
%global _python_bytecompile_extra 0
%define _unpackaged_files_terminate_build 0
%define _missing_doc_files_terminate_build 0

Name:           python3-proton-vpn-local-agent
Version:        1.6.3
Release:        1%{?dist}
Summary:        Proton VPN Local Agent Library
License:        GPL-3.0-or-later
URL:            https://protonvpn.com/
BuildArch:      noarch

Source0:        python3-proton-vpn-local-agent-upstream.rpm

BuildRequires:  cpio
BuildRequires:  rpm-build

Requires:       python3

%description
Proton VPN Local Agent daemon and IPC communication library.

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
find %{buildroot} -not -type d | sed "s|^%{buildroot}||" | sort -u > files.list

%files -f files.list

%changelog
* Wed Oct 21 2026 Saffet Yavuz <universish@github> - 0.2.0-1
- Repackaged for Copr.
