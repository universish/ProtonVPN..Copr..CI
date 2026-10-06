Name:           proton-vpn-gnome-desktop
Version:        4.4.4
Release:        1%{?dist}
Summary:        Proton VPN Linux Desktop application for GNOME and GTK environments
License:        GPL-3.0-or-later
URL:            https://protonvpn.com/
ExclusiveArch:  x86_64 aarch64

# scripts/orchestrator.py tarafından indirilen resmi upstream paketi
Source0:        proton-vpn-gnome-desktop-upstream.rpm

BuildRequires:  cpio
BuildRequires:  rpm-build
BuildRequires:  glib2-devel

# Temel Sistem ve Kimlik Doğrulama Bağımlılıkları
Requires:       gnome-keyring
Requires:       systemd-resolved
Requires:       NetworkManager
Requires:       NetworkManager-libnm
Requires:       libsecret

# Python ve GTK Çalışma Zamanı
Requires:       python3
Requires:       python3-gobject
Requires:       gtk3
Requires:       libappindicator-gtk3

# GNOME Tepsi ve Uzantı Bileşenleri
Requires:       gnome-shell-extension-appindicator
Requires:       gnome-extensions-app

%description
Official Proton VPN GUI desktop application client rebuilt for Fedora with
out-of-the-box systemd-resolved DNS leak protection and automatic GNOME
AppIndicator system integration.

%prep
%setup -c -T

%build
# İkili RPM içeriği paketlenmektedir

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}

# Upstream RPM içeriğini buildroot içine aç
cd %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idmv

# GNOME AppIndicator eklentisini sistem genelinde otomatik aktif eden GSchema override dosyasını oluştur
mkdir -p %{buildroot}%{_datadir}/glib-2.0/schemas
cat << 'EOF' > %{buildroot}%{_datadir}/glib-2.0/schemas/99-protonvpn-appindicator.gschema.override
[org.gnome.shell]
enabled-extensions=['appindicatorsupport@rgcjonas.gmail.com']
EOF

%post
if [ -x %{_bindir}/glib-compile-schemas ]; then
    %{_bindir}/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%postun
if [ -x %{_bindir}/glib-compile-schemas ]; then
    %{_bindir}/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%files
/*
%{_datadir}/glib-2.0/schemas/99-protonvpn-appindicator.gschema.override

%changelog
* Tue Oct 06 2026 Saffet Yavuz <universish@github> - 4.4.4-1
- Automated build with local upstream payload ingestion.
