%global debug_package %{nil}
%global __brp_python_bytecompile %{nil}
%global __brp_mangle_shebangs %{nil}
%global _python_bytecompile_extra 0
%define _unpackaged_files_terminate_build 0
%define _missing_doc_files_terminate_build 0

Name:           python3-proton-vpn-api-core
Version:        5.8.11
Release:        1%{?dist}
Summary:        Proton VPN Core API Library
License:        GPL-3.0-or-later
URL:            https://protonvpn.com/

Source0:        python3-proton-vpn-api-core-upstream.rpm

BuildRequires:  cpio
BuildRequires:  rpm-build
Requires:       python3
Requires:       python3-proton-core

%description
Core API and session manager for Proton VPN.

%prep
%setup -c -T

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
cd %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idmv || :

cd %{_builddir}/%{name}-%{version}
find %{buildroot} -not -type d | sed "s|^%{buildroot}||" | sort -u > files.list

%files -f files.list
