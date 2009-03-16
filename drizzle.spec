# TODO
# - prefix bin-commands with drizzle
# - changing paths (non-user stuff to sbindir)
# - logrotate
Summary:	A Lightweight SQL Database for Cloud and Web
Name:		drizzle
Version:	7.0.0
Release:	0.11
License:	GPL v2
Group:		Applications/Databases
Source0:	%{name}.tar.bz2
# Source0-md5:	0749fa072ec090f228e940cd34bbee13
Source1:	%{name}.init
Source2:	%{name}d.conf
Patch0:		%{name}-bools.patch
URL:		https://launchpad.net/drizzle
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	libevent-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	libuuid-devel
BuildRequires:	pcre-devel
BuildRequires:	protobuf
BuildRequires:	protobuf-devel
BuildRequires:	readline-devel
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	%{name}-libs = %{version}-%{release}
Requires:	rc-scripts
Provides:	group(drizzle)
Provides:	user(drizzle)
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
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig,drizzle} \
	   $RPM_BUILD_ROOT/var/{log/{archive,}/drizzle,lib/drizzle} \

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/drizzle
cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/drizzle/drizzled.conf

# am offers no way to install without .la (other than hook to rm -f)
rm -f $RPM_BUILD_ROOT%{_libdir}/drizzle/plugin/*.la

# we have our own better ones
rm $RPM_BUILD_ROOT%{_datadir}/drizzle/{drizzle-log-rotate,drizzle.server}
rm $RPM_BUILD_ROOT%{_bindir}/drizzled_safe
rm $RPM_BUILD_ROOT%{_bindir}/my_print_defaults
rm $RPM_BUILD_ROOT%{_bindir}/mysql_waitpid

# not useful
rm $RPM_BUILD_ROOT%{_libdir}/drizzle/plugin/libhello_world.so

%clean
rm -rf $RPM_BUILD_ROOT

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%pre
%groupadd -g 231 drizzle
%useradd -u 231 -d /var/lib/drizzle -s /bin/sh -g drizzle -c "Drizzle Server" drizzle

%post
/sbin/chkconfig --add drizzle
%service drizzle restart

%preun
if [ "$1" = "0" ]; then
	%service -q mysql drizzle
	/sbin/chkconfig --del drizzle
fi

%postun
if [ "$1" = "0" ]; then
	%userremove drizzle
	%groupremove drizzle
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS DRIZZLE.FAQ
%attr(755,root,root) %{_sbindir}/drizzled
%attr(754,root,root) /etc/rc.d/init.d/drizzle

%dir %{_sysconfdir}/drizzle
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/drizzle/drizzled.conf

%dir %{_libdir}/drizzle
%dir %{_libdir}/drizzle/plugin
%attr(755,root,root) %{_libdir}/drizzle/plugin/ha_blackhole.so
%attr(755,root,root) %{_libdir}/drizzle/plugin/libauth_pam.so
%attr(755,root,root) %{_libdir}/drizzle/plugin/liberrmsg_stderr.so
%attr(755,root,root) %{_libdir}/drizzle/plugin/liblogging_query.so
%attr(755,root,root) %{_libdir}/drizzle/plugin/libmd5udf.so

%attr(771,root,drizzle) /var/lib/drizzle
%attr(750,root,drizzle) %dir /var/log/drizzle
%attr(750,root,root) %dir /var/log/archive/drizzle

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libdrizzle.so.1
%attr(755,root,root) %{_libdir}/libdrizzle.so.*.*.*

%files client -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/drizzle
%attr(755,root,root) %{_bindir}/drizzleadmin
%attr(755,root,root) %{_bindir}/drizzlecheck
%attr(755,root,root) %{_bindir}/drizzledump
%attr(755,root,root) %{_bindir}/drizzledumpslow
%attr(755,root,root) %{_bindir}/drizzleimport
%attr(755,root,root) %{_bindir}/drizzleslap
%attr(755,root,root) %{_bindir}/drizzletest

# likely mysql pkg collisions
%attr(755,root,root) %{_bindir}/myisamchk
%attr(755,root,root) %{_bindir}/innochecksum

%files devel
%defattr(644,root,root,755)
%{_includedir}/drizzled
%{_includedir}/libdrizzle
%{_pkgconfigdir}/libdrizzle.pc
%{_aclocaldir}/drizzle.m4
%{_libdir}/libdrizzle.la
%{_libdir}/libdrizzle.so

# likely mysql-devel collisions
%{_includedir}/mystrings
%{_includedir}/mysys
