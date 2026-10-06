%global debug_package %{nil}

Name:           protonvpn-stable-release
Version:        1.0.4
Release:        1%{?dist}
Summary:        Proton VPN repository configuration and GPG keys (DPI-Bypass Safe Edition)
License:        GPL-3.0-or-later
URL:            https://protonvpn.com/
BuildArch:      noarch

%description
Repository configuration and OpenPGP keys for Proton VPN.
Configured with upstream disabled by default to prevent DPI SSL handshaking timeouts.

%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/yum.repos.d/
mkdir -p %{buildroot}%{_sysconfdir}/pki/rpm-gpg/

# Upstream deposu DPI engeline takıldığı için varsayılan olarak kapalı (enabled=0) tutulur
cat << 'EOF' > %{buildroot}%{_sysconfdir}/yum.repos.d/protonvpn-stable.repo
[protonvpn-fedora-stable]
name=ProtonVPN Fedora Stable (Official - Often DPI blocked)
baseurl=https://repo.protonvpn.com/fedora-$releasever-stable/
enabled=0
gpgcheck=1
repo_gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-ProtonVPN
EOF

# Resmi Proton GPG Genel Anahtarı (Fedora 44 / Stable)
cat << 'EOF' > %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-ProtonVPN
-----BEGIN PGP PUBLIC KEY BLOCK-----
Comment: Proton Technologies AG (Fedora 44) <opensource@proton.me>

mQINBGPV2jUBEADU+dE08G/E8kI0N7Tsl7Uq6J1cK1d...
... (Resmi anahtar bloğu veya lokal anahtar dosyası)
-----END PGP PUBLIC KEY BLOCK-----
EOF

%files
%{_sysconfdir}/yum.repos.d/protonvpn-stable.repo
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-ProtonVPN

%changelog
* Tue Oct 06 2026 Saffet Yavuz <universish@github> - 1.0.4-1
- Packaged repository config with disabled default state for DPI bypass.
