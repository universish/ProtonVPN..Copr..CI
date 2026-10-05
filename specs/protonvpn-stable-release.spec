Name:           protonvpn-stable-release
Version:        1.0.4
Release:        1%{?dist}
Summary:        Proton VPN repository and GPG key configuration
License:        GPL-3.0-or-later
URL:            https://protonvpn.com/
BuildArch:      noarch

%description
Repository configuration and OpenPGP keys for Proton VPN on Fedora.

%install
mkdir -p %{buildroot}%{_sysconfdir}/yum.repos.d/
mkdir -p %{buildroot}%{_sysconfdir}/pki/rpm-gpg/

cat << 'EOF' > %{buildroot}%{_sysconfdir}/yum.repos.d/protonvpn.repo
[protonvpn-fedora-stable]
name=ProtonVPN Fedora Stable repository
baseurl=https://repo.protonvpn.com/fedora-$releasever-stable/
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://repo.protonvpn.com/fedora-44-stable/public_key.asc
EOF

%files
%{_sysconfdir}/yum.repos.d/protonvpn.repo

%changelog
* Tue Oct 06 2026 Saffet Yavuz <universish@github> - 1.0.4-1
- Initial repository release configuration.
