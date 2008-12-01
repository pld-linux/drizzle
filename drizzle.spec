Summary:	A Lightweight SQL Database for Cloud and Web
Name:		drizzle
Version:	0
Release:	0.1
License:	GPL v2
Group:		Applications/Databases
Source0:	%{name}.tar.bz2
# Source0-md5:	749e9c0d3591f6381ee84a27abafd074
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

%prep
%setup -q -n %{name}

%build
%{__libtoolize} --automake
%{__aclocal} -I m4
%{__autoheader}
%{__automake}
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS CREDITS ChangeLog NEWS README THANKS TODO
