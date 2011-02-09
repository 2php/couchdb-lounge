RPM_SOURCE_DIR=`rpm --eval %{_sourcedir}`
RPM_LIB_DIR=`rpm --eval %{_libdir}`

COUCHDB_VERSION=`grep "Version" couchdb.spec | awk '{print $$2}'`
COUCHDB_GITHASH=`cd ../couchdb; git log --pretty=format:%h | head -1`
ifdef RELEASE
COUCHDB_RELEASE=${RELEASE}
else
COUCHDB_RELEASE=1
endif
COUCHDB_DIST_NAME=apache-couchdb-${COUCHDB_VERSION}
COUCHDB_RPM_TAG=`date +%Y%m%d`.${COUCHDB_RELEASE}.${COUCHDB_GITHASH}

submodule_couchdb:
	cd ..; git submodule init couchdb; git submodule update couchdb

dist_couchdb: submodule_couchdb
	cd ../couchdb; ./bootstrap; ./configure --libdir=${RPM_LIB_DIR}; make dist

couchdb: dist_couchdb	
	mkdir -p ${RPM_SOURCE_DIR}
	cp ../couchdb/${COUCHDB_DIST_NAME}.tar.gz ${RPM_SOURCE_DIR}/
	rpmbuild -ba couchdb.spec --define "tag ${COUCHDB_RPM_TAG}"

