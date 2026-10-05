Name:           proton-vpn-gnome-desktop
Version:        4.4.4
Release:        1%{?dist}
Summary:        Proton VPN Linux Desktop application for GNOME and GTK environments
License:        GPL-3.0-or-later
URL:            https://protonvpn.com/
ExclusiveArch:  x86_64 aarch64

# Resmi Proton deposundan upstream kaynak
Source0:        https://repo.protonvpn.com/fedora-44-stable/protonvpn-stable-release/proton-vpn-gnome-desktop-%{version}.%{_arch}.rpm

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

# Otomatik GNOME uzantı aktivasyonu için şema
Source1:        99-protonvpn-appindicator.gschema.override

%description
Official Proton VPN GUI desktop application client rebuilt for Fedora with
out-of-the-box systemd-resolved DNS leak protection and automatic GNOME
AppIndicator system integration.

%prep
# Boş prep adımı; kaynak RPM install aşamasında açılacaktır
%setup -c -T

%build
# Derleme gerektirmez, ikili RPM paketi dönüştürülmektedir

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}

# Upstream RPM içeriğini dışa aktar
cd %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idmv

# GNOME AppIndicator eklentisini sistem genelinde otomatik aktif eden GSchema override dosyasını ekle
mkdir -p %{buildroot}%{_datadir}/glib-2.0/schemas
cat << 'EOF' > %{buildroot}%{_datadir}/glib-2.0/schemas/99-protonvpn-appindicator.gschema.override
[org.gnome.shell]
enabled-extensions=['appindicatorsupport@rgcjonas.gmail.com']
EOF

%post
# GSchema önbelleğini yeniden derle (Uzantının otomatik devreye girmesi için)
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
- Automated build with full dependency pinning and auto-activated AppIndicator.
