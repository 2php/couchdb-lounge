#!/bin/sh

VERSION=`grep "Version" lounge-replicator.spec | awk '{print $2}'`
RPMBUILDDIR=`rpm --eval "%{_topdir}"`
SOURCE_TARBALL=rn.tar.gz
DIR=lounge-replicator-$VERSION/

rm -f $SOURCE_TARBALL 
rm -rf $DIR

mkdir $DIR
cp continuous_replicator.py $DIR
cp replicator.logrotate $DIR
tar czf rn.tar.gz $DIR

rm -f $RPMBUILDDIR/SOURCES/$DIR || true
cp $SOURCE_TARBALL $RPMBUILDDIR/SOURCES
rpmbuild -ba --clean --rmsource lounge-replicator.spec
rm -f $SOURCE_TARBALL
rm -rf $DIR
