#
# spec file for package telnet-server-ssl
#
# Copyright (c) Barry Nelson
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.


Name:           telnet-ssl
Version:        0.17.42
Release:        1.0
Summary:        SSL Telnet server
License:        GPL-2.0-only
Group:          Productivity/Networking/Other
Source:         netkit-telnet-ssl-SuSE.tgz
Source1:	generate_cert.sh
BuildRequires:  cmake
BuildRequires:  libopenssl-3-devel
BuildRequires:  ncurses-devel
Requires:	libopenssl3
Requires:	ncurses

%description
Netkit telnet SSL (netkit-telnet-ssl) is an implementation of the telnet
protocol for logging into remote systems which supports SSL.

%package server
Summary:        A Server Program for the Telnet Remote Login Protocol
Group:          Productivity/Networking/Other
Requires:       netcfg
Requires:       util-linux
Requires:	libopenssl3
Requires:	openssl
Provides:       nkitserv:%{_sbindir}/in.telnetd
Obsoletes:      nkitserv

%description server
Netkit telnet server SSL (netkit-telnet-ssl-server) is an SSL telnet server.

%prep
%setup -q

%build
export CPPFLAGS="-I/usr/include/libseccomp"
export CFLAGS="-I/usr/include/libseccomp -L/usr/lib64"
export LDFLAGS="-L/usr/lib64"
./configure --prefix=/usr

cmake . --install-prefix /usr

make V=1 %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/bin/telnetlogin || true
rm -f %{buildroot}/usr/share/man/man8/telnetlogin.8 || true

install -d %{buildroot}%{_sysconfdir}/telnetd-ssl
mkdir -p %{buildroot}/usr/lib
mkdir -p %{buildroot}/etc/xinetd.d
cat >%{buildroot}/etc/xinetd.d/telnets <<@EOF@
# default: on
# description: TelnetS is a secure SSL login server.
service telnets
{
        socket_type     = stream
        protocol        = tcp
        wait            = no
        user            = root
        server          = /usr/sbin/in.telnetd
        server_args     = -N -z secure -z ssl
        disable         = yes
}
@EOF@
ln -s /bin/login %{buildroot}/usr/lib/telnetlogin
mkdir -p %{buildroot}/etc/telnetd-ssl
cp %{SOURCE1} %{buildroot}/etc/telnetd-ssl/generate_cert.sh
chmod 755 %{buildroot}/etc/telnetd-ssl/generate_cert.sh

%pre

%post
chmod 755 /etc/telnetd-ssl/generate_cert.sh
/etc/telnetd-ssl/generate_cert.sh /etc/telnetd-ssl/telnetd.pem || true
chmod 600 /etc/telnetd-ssl/telnetd.pem

%preun

%postun

%files
%defattr(-,root,root)
/usr/bin/telnet-ssl
/usr/share/man/man1/telnet-ssl.1.gz

%files server
/usr/sbin/in.telnetd
/usr/share/man/man5/issue.net.5.gz
/usr/share/man/man8/in.telnetd.8.gz
/etc/telnetd-ssl/generate_cert.sh
%config(noreplace) /usr/lib/telnetlogin
%config(noreplace) /etc/xinetd.d/telnets

%changelog
