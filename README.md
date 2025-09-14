netkit-telnet-ssl
=================

This is https://packages.debian.org/source/sid/netkit-telnet , with some
bugfixes and SSL support.

*Note:* This is the `netkit-telnet-ssl` package, which adds an argument if you want to
make a telnet connection over SSL.

* netkit-telnet-ssl: https://github.com/marado/netkit-telnet-ssl
\
To build unpack the source code and run:\
./configure --prefix=/usr\
cmake . --install-prefix /usr\
make\
\
To install run make install, then run:\
./SOURCES/generate_cert.sh /etc/telnetd-ssl/telnetd.pem\
\
On SuSE Leap Linux you need to will create a file /etc/xinetd.d/telnets with the following contents:\
\
\# default: on\
\# description: TelnetS is a secure SSL login server.\
service telnets\
{\
        socket_type     = stream\
        protocol        = tcp\
        wait            = no\
        user            = root\
        server          = /usr/sbin/in.telnetd\
        server_args     = -L /bin/login -N -z secure -z ssl\
        disable         = no\
}

On modern CentOS and Redhat Linux you will need to create a systemd socket definition. SuSE also supports systemd sockets but also supports xinetd.

You may want to install a CA signed certificate and key into /etc/telnetd-ssl/telnetd.pem since the generate_cert.sh script only installs a self signed one.
