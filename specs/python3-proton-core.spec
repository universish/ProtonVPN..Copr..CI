%global debug_package %{nil}
%global __brp_python_bytecompile %{nil}
%global __brp_mangle_shebangs %{nil}
%global _python_bytecompile_extra 0
%define _unpackaged_files_terminate_build 0
%define _missing_doc_files_terminate_build 0

Name:           python3-proton-core
Version:        0.7.4
Release:        1%{?dist}
Summary:        Proton Core Python Library
License:        GPL-3.0-or-later
URL:            https://protonvpn.com/
BuildArch:      noarch

Source0:        python3-proton-core-upstream.rpm

BuildRequires:  cpio
BuildRequires:  rpm-build
Requires:       python3

Provides:       python3dist(proton-core) = %{version}
Provides:       python3.14dist(proton-core) = %{version}

%description
Proton Core Python Library providing authentication and session APIs.

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
