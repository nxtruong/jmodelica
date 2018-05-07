# 
#    Copyright (C) 2018 Modelon AB
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the Common Public License as published by
#    IBM, version 1.0 of the License.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY. See the Common Public License for more details.
#
#    You should have received a copy of the Common Public License
#    along with this program.  If not, see
#     <http://www.ibm.com/developerworks/library/os-cpl.html/>.
BUILD_PKGS_JM_COMMON="cmake swig ant wget tar which patch"
BUILD_PKGS_JM_CENTOS="subversion-devel gcc-c++ gcc-gfortran python-ipython java-1.8.0-openjdk python-devel numpy scipy matplotlib Cython python-lxml python-nose python-jpype zlib-devel boost-devel"
BUILD_PKGS_JM_UBUNTU="subversion g++ gfortran ipython openjdk-8-jdk python-dev python-numpy python-scipy python-matplotlib cython python-lxml python-nose python-jpype zlib1g-dev libboost-dev"

LINUX_DISTRIBUTION=UNKNOWN

if [ -f /etc/centos-release ]; then
	LINUX_DISTRIBUTION=CENTOS
elif [-f /etc/redhat-release ]; then 
	LINUX_DISTRIBUTION=REDHAT
elif [-f /etc/debian_version ]; then 
	LINUX_RELEASE=DEBIAN
else 
	echo ERROR: current linux distribution not supported yet 
fi

if [[ "$LINUX_DISTRIBUTION" == CENTOS ]] || [[ "$LINUX_DISTRIBUTION" == CENTOS ]] ; then 
	yum install -y $BUILD_PKGS_JM_COMMON 
	yum install -y $BUILD_PKGS_JM_CENTOS 
elif  [[ "$LINUX_DISTRIBUTION" == CENTOS ]]; then  
	apt-get install $BUILD_PKGS_JM_COMMON
	apt-get install $BUILD_PKGS_JM_UBUNTU
fi
