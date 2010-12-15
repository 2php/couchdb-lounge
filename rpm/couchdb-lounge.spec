Name:		couchdb-lounge1
Version: 	1.4.0
Release:	3%{?dist}
Summary:	Clustered CouchDB
Group: 		Database/CouchDBCluster
License: 	Apache

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:  lounge-dumbproxy1 >= 1.4.0, lounge-smartproxy1 >= 1.4.0, couchdb >= 0.10.2, lounge-replicator >= 1.4.0
Obsoletes: couchdb-lounge < 1.4.0
Conflicts: couchdb-lounge2
Provides: couchdb-lounge = %{version}

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
%config/etc/couchdb/default.d/lounge.ini

