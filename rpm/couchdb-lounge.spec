Name:		couchdb-lounge-transitional
Version: 	2.0
Release:	3%{?dist}
Summary:	Clustered CouchDB
Group: 		Database/CouchDBCluster
License: 	Apache

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:  lounge-dumbproxy-transitional >= 2.0, lounge-smartproxy-transitional >= 2.0, couchdb >= 0.10.0, lounge-replicator >= 1.2.0
Conflicts: couchdb-lounge < 2.0

%description
Metapackage wrapping the dependencies for the various lounge components

%prep
cp -p %{_sourcedir}/lounge.ini .

%build

%clean

%install
mkdir -p %{buildroot}/etc/couchdb/default.d
cp %{_builddir}/lounge.ini %{buildroot}/etc/couchdb/default.d/lounge.ini

%post
/etc/init.d/couchdb stop
/etc/init.d/couchdb start
/etc/init.d/smartproxyd restart
/etc/init.d/dumbproxy restart

%files
/etc/couchdb/default.d/lounge.ini

