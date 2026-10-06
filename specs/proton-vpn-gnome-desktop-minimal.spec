%global debug_package %{nil}

Name:           proton-vpn-gnome-desktop
Version:        0.11.0
Release:        1%{?dist}
Summary:        Proton VPN Linux Desktop application for GNOME and GTK environments
License:        GPL-3.0-or-later
URL:            https://protonvpn.com/
ExclusiveArch:  x86_64 aarch64 noarch

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

# Python ve Masaüstü Bağımlılıkları
Requires:       python3
Requires:       python3-gobject
Requires:       gtk3
Requires:       libappindicator-gtk3
Requires:       gnome-shell-extension-appindicator
Requires:       gnome-extensions-app

%description
Official Proton VPN GUI desktop application client rebuilt for Fedora with
out-of-the-box systemd-resolved DNS leak protection and automatic GNOME
AppIndicator system integration.

%prep
%setup -c -T

%build
# İkili RPM içeriği dönüştürülüyor

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}

# Upstream RPM içeriğini aç
cd %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idmv || :

# GNOME AppIndicator otomatik aktivasyon şeması
mkdir -p %{buildroot}%{_datadir}/glib-2.0/schemas
cat << 'EOF' > %{buildroot}%{_datadir}/glib-2.0/schemas/99-protonvpn-appindicator.gschema.override
[org.gnome.shell]
enabled-extensions=['appindicatorsupport@rgcjonas.gmail.com']
EOF

# Sistem dizinleriyle çakışmayan dinamik dosya listesi üret
find %{buildroot} -not -type d | sed "s|^%{buildroot}||" > %{_builddir}/files.list

%post
if [ -x %{_bindir}/glib-compile-schemas ]; then
    %{_bindir}/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%postun
if [ -x %{_bindir}/glib-compile-schemas ]; then
    %{_bindir}/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%files -f %{_builddir}/files.list

%changelog
* Tue Oct 06 2026 Saffet Yavuz <universish@github> - 0.11.0-1
- Fixed debug_package generation and dynamic file listing.
