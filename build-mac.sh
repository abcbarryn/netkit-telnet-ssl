#!/bin/sh

cp CMakeLists.MacOS CMakeLists.txt
rm -f telnet/staticlib
mkdir telnet/staticlib
ln -s /opt/homebrew/lib/*.a telnet/staticlib
make
