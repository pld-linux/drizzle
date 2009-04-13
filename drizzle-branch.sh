#!/bin/sh
set -e

t=$(mktemp -d)
p=$(basename $0 .sh)
d=drizzle

if [ ! -d $d ]; then
	bzr clone lp:drizzle $d
fi

bzr clone $d $t/$p

# generate m4/bzr_version.m4
cd $t/$p
LIBTOOLIZE=true ACLOCAL=true AUTOHEADER=true AUTOMAKE=true AUTOCONF=true sh config/autorun.sh
cd -

tar -cjf $p.tar.bz2 -C $t --exclude=.bzr $p/

rm -rf $t
