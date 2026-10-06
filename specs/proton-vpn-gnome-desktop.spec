%global debug_package %{nil}
%global _python_bytecompile_extra 0

Name:           proton-vpn-gnome-desktop
Version:        0.11.0
Release:        1%{?dist}
Summary:        Proton VPN Linux Desktop application for GNOME and GTK environments
License:        GPL-3.0-or-later
URL:            https://protonvpn.com/
BuildArch:      noarch

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
# No compilation needed for binary/noarch payload

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}

# 1. Upstream RPM içeriğini aç
cd %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idmv || :

# 2. GNOME AppIndicator otomatik aktivasyon şeması
mkdir -p %{buildroot}%{_datadir}/glib-2.0/schemas
cat << 'EOF' > %{buildroot}%{_datadir}/glib-2.0/schemas/99-protonvpn-appindicator.gschema.override
[org.gnome.shell]
enabled-extensions=['appindicatorsupport@rgcjonas.gmail.com']
EOF

# 3. Metapaket boş dosya hatasını (Empty %files) önlemek için belge dosyası
mkdir -p %{buildroot}%{_docdir}/%{name}
echo "Repackaged by universish ProtonVPN Copr CI" > %{buildroot}%{_docdir}/%{name}/README.copr

# 4. Dosya listesini build çalışma dizinine yaz
cd %{_builddir}/%{name}-%{version}
find %{buildroot} -type f -o -type l | sed "s|^%{buildroot}||" > files.list

%post
if [ -x %{_bindir}/glib-compile-schemas ]; then
    %{_bindir}/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%postun
if [ -x %{_bindir}/glib-compile-schemas ]; then
    %{_bindir}/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%files -f files.list

%changelog
* Tue Oct 06 2026 Saffet Yavuz <universish@github> - 0.11.0-1
- Converted to pure noarch and corrected files.list pathing.
