#!/bin/bash
# Install script for Jackson dependencies.
# This was created for Raspbian Jessie Stretch lite, June 2018 release.
# Other releases may or may not work without modification.
set -e

if [[ $EUID -ne 0 ]]; then
   echo 'You must run this as root with sudo ./install.sh'
   exit 1
fi

echo 'Update apt packages and install necessary dependencies...'
apt-get update
apt-get install -y build-essential automake autoconf libtool bison swig python3 python3-dev python3-pip python3-numpy libpulse-dev libasound2-dev git scons

echo 'Download sphinxbase and pocketsphinx source...'
mkdir -p ./pocketsphinx_source
cd ./pocketsphinx_source
wget https://downloads.sourceforge.net/project/cmusphinx/sphinxbase/5prealpha/sphinxbase-5prealpha.tar.gz
wget https://downloads.sourceforge.net/project/cmusphinx/pocketsphinx/5prealpha/pocketsphinx-5prealpha.tar.gz

echo 'Unarchive and install sphinxbase...'
tar xfz sphinxbase-5prealpha.tar.gz
cd ./sphinxbase-5prealpha
./autogen.sh PYTHON=/usr/bin/python3
make
make install
cd ..

echo 'Unarchive and install pocketsphinx...'
tar xfz pocketsphinx-5prealpha.tar.gz
cd ./pocketsphinx-5prealpha
./autogen.sh PYTHON=/usr/bin/python3
make
make install
ldconfig
cd ../..

# Fix issue with pocketsphinx python library installed into site-packages vs.
# the necessary dist-packages folder in Debian/Raspbian.
echo '../site-packages' > /usr/local/lib/python3.5/dist-packages/site-packages.pth

echo 'Clone and install rpi_ws281x neopixel library...'
git clone https://github.com/jgarff/rpi_ws281x.git
cd ./rpi_ws281x
scons
cd ./python
python3 setup.py install

echo 'Install other Python dependencies...'
pip3 install pyalsaaudio
