%define couchdb_user couchdb
%define couchdb_group couchdb
%define couchdb_home %{_localstatedir}/lib/couchdb
Name:           couchdb
Version:        1.0.2
Release:        1%{?dist}
Summary:        A document database server, accessible via a RESTful JSON API

Group:          Applications/Databases
License:        ASL 2.0
URL:            http://couchdb.apache.org/
Source0:        http://www.apache.org/dist/%{name}/%{version}/apache-%{name}-%{version}.tar.gz
Patch1:         couchdb-0001-Force-init-script-installation.patch
Patch2:         couchdb-0002-Install-into-erllibdir-by-default.patch
Patch3:         couchdb-0003-Remove-bundled-erlang-oauth-library.patch
Patch4:         couchdb-0004-Remove-bundled-erlang-etap-library.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  autoconf
BuildRequires:  automake >= 1.6.3
BuildRequires:  erlang
BuildRequires:  gcc
BuildRequires:  js-devel >= 1.7
BuildRequires:  libicu-devel >= 3.0
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  pkgconfig
BuildRequires:  which
BuildRequires:  help2man
BuildRequires:  curl-devel
BuildRequires(check):  erlang-etap

Requires:       erlang
Requires:       erlang-oauth
# For %{_bindir}/icu-config
Requires:       libicu-devel
Requires:       logrotate

#Initscripts
Requires(post): chkconfig
Requires(preun): chkconfig initscripts
Requires: lsb

# Users and groups
Requires(pre): shadow-utils


%description
Apache CouchDB is a document-oriented database that can be queried and indexed
in a MapReduce fashion using JavaScript. CouchDB also offers incremental
replication with bi-directional conflict detection and resolution.

CouchDB provides a RESTful JSON API than can be accessed from any environment
that allows HTTP requests. There are myriad third-party client libraries that
make this even easier from your programming language of choice. CouchDB’s built
in Web administration console speaks directly to the database using HTTP
requests issued from your browser.

%prep
%setup -q -n apache-%{name}-%{version}
%patch1 -p1 -b .initenabled
%patch2 -p1 -b .fix_lib_path
%patch3 -p1 -b .remove_bundled_oauth
%patch4 -p1 -b .remove_bundled_etap
rm -rf src/erlang-oauth
rm -rf src/etap
# Restore original timestamps to avoid reconfiguring
touch -r configure.ac.initenabled configure.ac
touch -r configure.fix_lib_path configure


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

## Use /etc/init.d instead of /etc/rc.d
mkdir -p $RPM_BUILD_ROOT%{_initrddir}
mv $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/couchdb \
$RPM_BUILD_ROOT%{_initrddir}/couchdb

## Use /etc/sysconfig instead of /etc/default
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
mv $RPM_BUILD_ROOT%{_sysconfdir}/default/couchdb \
$RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/couchdb
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/default

# Remove unecessary files
rm -rf  $RPM_BUILD_ROOT%{_datadir}/doc/couchdb

# clean-up .la archives
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%check
make check


%clean
rm -rf $RPM_BUILD_ROOT


%pre
getent group %{couchdb_group} >/dev/null || groupadd -r %{couchdb_group}
getent passwd %{couchdb_user} >/dev/null || \
useradd -r -g %{couchdb_group} -d %{couchdb_home} -s /bin/bash \
-c "Couchdb Database Server" %{couchdb_user}
exit 0


%post
/sbin/ldconfig
/sbin/chkconfig --add couchdb


%postun -p /sbin/ldconfig


%preun
if [ $1 = 0 ] ; then
    /sbin/service couchdb stop >/dev/null 2>&1
    /sbin/chkconfig --del couchdb
fi


%files
%defattr(-,root,root,-)
%doc AUTHORS BUGS CHANGES LICENSE NEWS NOTICE README THANKS
%dir %{_sysconfdir}/couchdb
%dir %{_sysconfdir}/couchdb/local.d
%dir %{_sysconfdir}/couchdb/default.d
%config(noreplace) %attr(0644, %{couchdb_user}, root) %{_sysconfdir}/couchdb/default.ini
%config(noreplace) %attr(0644, %{couchdb_user}, root) %{_sysconfdir}/couchdb/local.ini
%config(noreplace) %{_sysconfdir}/sysconfig/couchdb
%config(noreplace) %{_sysconfdir}/logrotate.d/couchdb
%{_initrddir}/couchdb
%{_bindir}/*
%{_libdir}/erlang/lib/*
%{_datadir}/couchdb
%{_mandir}/man1/*
%dir %attr(0755, %{couchdb_user}, root) %{_localstatedir}/log/couchdb
%dir %attr(0755, %{couchdb_user}, root) %{_localstatedir}/run/couchdb
%dir %attr(0755, %{couchdb_user}, root) %{_localstatedir}/lib/couchdb

%changelog
* Tue Feb  1 2011 Randall Leeds <randall@meebo-inc.com> 1.0.2-1
- Update to vanilla upstream 1.0.2

* Tue Jun  1 2010 Peter Lemenkov <lemenkov@gmail.com> 0.10.2-8
- Suppress unneeded message while stopping CouchDB via init-script

* Mon May 31 2010 Peter Lemenkov <lemenkov@gmail.com> 0.10.2-7
- Do not manually remove pid-file while stopping CouchDB

* Mon May 31 2010 Peter Lemenkov <lemenkov@gmail.com> 0.10.2-6
- Fix 'stop' and 'status' targets in the init-script (see rhbz #591026)

* Fri May 28 2010 Randall Leeds <randall.leeds@gmail.com> 0.10.2-1-5
- Update replication fixes patch to bail on checkpoint conflict

* Thu May 27 2010 Randall Leeds <randall.leeds@gmail.com> 0.10.2-1-4
- su instead of daemon in couchdb.init, let couch manage daemonizing
- use COUCHDB_USER variable from /etc/sysconfig/couchdb

* Wed May 26 2010 Randall Leeds <randall.leeds@gmail.com> 0.10.2-1-3
- fix regression in replication fixes patch

* Tue May 25 2010 Randall Leeds <randall.leeds@gmail.com> 0.10.2-1-2
- add synchronous logging patch

* Tue May 25 2010 Randall Leeds <randall.leeds@gmail.com> 0.10.2-1-1
- fold checkpoints into rep-fixes patch

* Thu May 14 2010 Peter Lemenkov <lemenkov@gmail.com> 0.10.2-4
- Use system-wide erlang-oauth instead of bundled copy

* Thu May 13 2010 Peter Lemenkov <lemenkov@gmail.com> 0.10.2-3
- Fixed init-script to use /etc/sysconfig/couchdb values (see rhbz #583004)
- Fixed installation location of beam-files (moved to erlang directory)

* Fri May  7 2010 Peter Lemenkov <lemenkov@gmail.com> 0.10.2-2
- Remove useless BuildRequires

* Fri May  7 2010 Peter Lemenkov <lemenkov@gmail.com> 0.10.2-1
- Update to 0.10.2 (resolves rhbz #578580 and #572176)
- Fixed chkconfig priority (see rhbz #579568)

* Tue Apr 27 2010 Randall Leeds <randall.leeds@gmail.com> 0.10.1-13-2
- bump checkpoint history limit back up to 50

* Fri Apr 09 2010 Randall Leeds <randall.leeds@gmail.com> 0.10.1-13
- quote ulimit check in init script

* Fri Apr 09 2010 Randall Leeds <randall.leeds@gmail.com> 0.10.1-12
- Patch to fix HTTP Keep-Alive problem with replication

* Fri Apr 09 2010 Randall Leeds <randall.leeds@gmail.com> 0.10.1-11
- Init script supports standard couchdb sysconfig options + ulimit

* Fri Mar 26 2010 Kevin Ferguson <kevin.a.ferguson@gmail.com> 0.10.1-7
- Init script tweaks

* Wed Mar 10 2010 Kevin Ferguson <kevin.a.ferguson@gmail.com> 0.10.1-5
- Backport replication checkpointing fix

* Tue Mar 09 2010 Kevin Ferguson <kevin.a.ferguson@gmail.com> 0.10.1-3
- Backport mochiweb max conn fix

* Fri Mar 05 2010 Kevin Ferguson <kevin.a.ferguson@gmail.com> 0.10.1-2
- Backport http://issues.apache.org/jira/browse/COUCHDB-597

* Thu Dec 03 2009 Randall Leeds <randall.leeds@gmail.com> 0.10.1-1
- Update to 0.10.1
- Remove %config(noreplace) from default.ini

* Thu Oct 15 2009 Allisson Azevedo <allisson@gmail.com> 0.10.0-2
- Added patch to force init_enabled=true in configure.ac.

* Thu Oct 15 2009 Allisson Azevedo <allisson@gmail.com> 0.10.0-1
- Update to 0.10.0.

* Sun Oct 04 2009 Rahul Sundaram <sundaram@fedoraproject.org> 0.9.1-2
- Change url. Fixes rhbz#525949

* Thu Jul 30 2009 Allisson Azevedo <allisson@gmail.com> 0.9.1-1
- Update to 0.9.1.
- Drop couchdb-0.9.0-pid.patch.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 21 2009 Allisson Azevedo <allisson@gmail.com> 0.9.0-2
- Fix permission for ini files.
- Fix couchdb.init start process.

* Tue Apr 21 2009 Allisson Azevedo <allisson@gmail.com> 0.9.0-1
- Update to 0.9.0.

* Tue Nov 25 2008 Allisson Azevedo <allisson@gmail.com> 0.8.1-4
- Use /etc/sysconfig for settings.

* Tue Nov 25 2008 Allisson Azevedo <allisson@gmail.com> 0.8.1-3
- Fix couchdb_home.
- Added libicu-devel for requires.

* Tue Nov 25 2008 Allisson Azevedo <allisson@gmail.com> 0.8.1-2
- Fix spec issues.

* Tue Nov 25 2008 Allisson Azevedo <allisson@gmail.com> 0.8.1-1
- Initial RPM release
