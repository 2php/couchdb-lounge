Name:		couchdb-lounge2
Version: 	2.1
Release:	3%{?dist}
Summary:	Clustered CouchDB
Group: 		Database/CouchDBCluster
License: 	Apache

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:  lounge-dumbproxy >= 2.1, lounge-smartproxy >= 2.1, couchdb >= 0.10.2, lounge-replicator >= 1.2.0
Obsoletes: couchdb-lounge1
Obsoletes: couchdb-lounge < 2.1
Obsoletes: couchdb-lounge-transitional
Provides: couchdb-lounge = %{version}

%description
Metapackage wrapping the dependencies for the various lounge components

%prep
cp -p %{_sourcedir}/lounge.ini .

%build

%clean

%install
mkdir -p %{buildroot}/etc/couchdb/default.d
mkdir -p %{buildroot}/var/run/lounge
mkdir -p %{buildroot}/var/log/lounge
cp %{_builddir}/lounge.ini %{buildroot}/etc/couchdb/default.d/lounge.ini

%post
/etc/init.d/couchdb stop
/etc/init.d/couchdb start
/etc/init.d/smartproxyd restart
/etc/init.d/dumbproxy restart

%files
%dir /var/run/lounge
%dir /var/log/lounge
/etc/couchdb/default.d/lounge.ini

