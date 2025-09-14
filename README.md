netkit-telnet-ssl
=================

This is https://packages.debian.org/source/sid/netkit-telnet , with some
bugfixes and SSL support.

*Note:* This is the `netkit-telnet-ssl` package, whichadds an argument if you want to
make a telnet connection over SSL.

* netkit-telnet-ssl: https://github.com/marado/netkit-telnet-ssl

To build unpack the source code and run:
./configure --prefix=/usr
cmake . --install-prefix /usr
make

To install run make install, then run:
./SOURCES/generate_cert.sh /etc/telnetd-ssl/telnetd.pem
I suggest also creating a file /etc/xinetd.d/telnets with the following contents:

# default: on
# description: TelnetS is a secure SSL login server.
service telnets
{
        socket_type     = stream
        protocol        = tcp
        wait            = no
        user            = root
        server          = /usr/sbin/in.telnetd
        server_args     = -L /bin/login -N -z secure -z ssl
        disable         = no
}
