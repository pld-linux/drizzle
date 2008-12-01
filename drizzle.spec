# TODO
# - finish packaging
Summary:	A Lightweight SQL Database for Cloud and Web
Name:		drizzle
Version:	0
Release:	0.1
License:	GPL v2
Group:		Applications/Databases
Source0:	%{name}.tar.bz2
# Source0-md5:	749e9c0d3591f6381ee84a27abafd074
Patch0:		%{name}-ncurses.patch
Patch1:		%{name}-readline-ac-cache.patch
Patch2:		%{name}-bools.patch
Patch3:		%{name}-zlibs.patch
URL:		https://launchpad.net/drizzle
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	protobuf
BuildRequires:	protobuf-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Drizzle project is building a database optimized for Cloud and Net
applications. It is being designed for massive concurrency on modern
multi-cpu/core architecture. The code is originally derived from
MySQL.

The project is focused on making a database that is:
- Reliable
- Fast and scalable on modern architecture
- Simply design for ease of installation and management

%package client
Summary:	Drizzle - Client
Group:		Applications/Databases
Requires:	%{name}-libs = %{version}-%{release}

%description client
This package contains the standard Drizzle clients.

%package libs
Summary:	Shared libraries for Drizzle
Group:		Libraries

%description libs
Shared libraries for Drizzle.

%package devel
Summary:	Drizzle - Development header files and libraries
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This package contains the development header files and libraries
necessary to develop Drizzle client applications.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS DRIZZLE.FAQ
%attr(755,root,root) %{_sbindir}/drizzled
%dir %{_libdir}/drizzle
%dir %{_libdir}/drizzle/plugin
%attr(755,root,root) %{_libdir}/drizzle/plugin/ha_blackhole.so
%attr(755,root,root) %{_libdir}/drizzle/plugin/ha_blackhole.so.*.*.*
%attr(755,root,root) %{_libdir}/drizzle/plugin/ha_blackhole.so.0
%attr(755,root,root) %{_libdir}/drizzle/plugin/libauth_pam.so
%attr(755,root,root) %{_libdir}/drizzle/plugin/libauth_pam.so.*.*.*
%attr(755,root,root) %{_libdir}/drizzle/plugin/libauth_pam.so.0
%attr(755,root,root) %{_libdir}/drizzle/plugin/liberrmsg_stderr.so
%attr(755,root,root) %{_libdir}/drizzle/plugin/liberrmsg_stderr.so.*.*.*
%attr(755,root,root) %{_libdir}/drizzle/plugin/liberrmsg_stderr.so.0
%attr(755,root,root) %{_libdir}/drizzle/plugin/libhello_world.so
%attr(755,root,root) %{_libdir}/drizzle/plugin/libhello_world.so.*.*.*
%attr(755,root,root) %{_libdir}/drizzle/plugin/libhello_world.so.0
%attr(755,root,root) %{_libdir}/drizzle/plugin/liblogging_query.so
%attr(755,root,root) %{_libdir}/drizzle/plugin/liblogging_query.so.*.*.*
%attr(755,root,root) %{_libdir}/drizzle/plugin/liblogging_query.so.0
%attr(755,root,root) %{_libdir}/drizzle/plugin/libmd5udf.so
%attr(755,root,root) %{_libdir}/drizzle/plugin/libmd5udf.so.*.*.*
%attr(755,root,root) %{_libdir}/drizzle/plugin/libmd5udf.so.0

%dir %{_datadir}/drizzle
%{_datadir}/drizzle/drizzle-log-rotate
%{_datadir}/drizzle/drizzle.server

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libdrizzle.so.1
%attr(755,root,root) %{_libdir}/libdrizzle.so.*.*.*

%files client -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/binlog_reader
%attr(755,root,root) %{_bindir}/binlog_writer
%attr(755,root,root) %{_bindir}/drizzle
%attr(755,root,root) %{_bindir}/drizzleadmin
%attr(755,root,root) %{_bindir}/drizzlecheck
%attr(755,root,root) %{_bindir}/drizzled_safe
%attr(755,root,root) %{_bindir}/drizzledump
%attr(755,root,root) %{_bindir}/drizzledumpslow
%attr(755,root,root) %{_bindir}/drizzleimport
%attr(755,root,root) %{_bindir}/drizzleslap
%attr(755,root,root) %{_bindir}/drizzletest
%attr(755,root,root) %{_bindir}/innochecksum
%attr(755,root,root) %{_bindir}/master_list_reader
%attr(755,root,root) %{_bindir}/master_list_writer
%attr(755,root,root) %{_bindir}/schema_reader
%attr(755,root,root) %{_bindir}/table_reader
%attr(755,root,root) %{_bindir}/table_writer

# likely mysql-devel collisions
%attr(755,root,root) %{_bindir}/my_print_defaults
%attr(755,root,root) %{_bindir}/myisamchk
%attr(755,root,root) %{_bindir}/mysql_waitpid

%files devel
%defattr(644,root,root,755)
%{_includedir}/drizzled
%{_includedir}/libdrizzle
# likely mysql-devel collisions
%{_includedir}/mystrings
%{_includedir}/mysys
%{_pkgconfigdir}/libdrizzle.pc
%{_aclocaldir}/drizzle.m4
%{_libdir}/drizzle/plugin/ha_blackhole.la
%{_libdir}/drizzle/plugin/libauth_pam.la
%{_libdir}/drizzle/plugin/liberrmsg_stderr.la
%{_libdir}/drizzle/plugin/libhello_world.la
%{_libdir}/drizzle/plugin/liblogging_query.la
%{_libdir}/drizzle/plugin/libmd5udf.la
%{_libdir}/libdrizzle.la
%{_libdir}/libdrizzle.so
