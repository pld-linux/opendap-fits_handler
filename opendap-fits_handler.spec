#
# Conditional build:
%bcond_with	tests	# make check (requires BES server)
#
Summary:	FITS data handler module for the OPeNDAP data server
Summary(pl.UTF-8):	Moduł obsługujący dane FITS dla serwera danych OPeNDAP
Name:		opendap-fits_handler
Version:	1.0.11
Release:	3
License:	LGPL v2.1+
Group:		Daemons
Source0:	http://www.opendap.org/pub/source/fits_handler-%{version}.tar.gz
# Source0-md5:	47b7e4730db6babd1a2716c0725473e3
URL:		http://opendap.org/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.10
%{?with_tests:BuildRequires:	bes >= 3.13.0}
BuildRequires:	bes-devel >= 3.13.0
BuildRequires:	cfitsio-devel
BuildRequires:	libdap-devel >= 3.13.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	pkgconfig
Requires:	bes >= 3.13.0
Requires:	libdap >= 3.13.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the FITS data handler module for the OPeNDAP data server. It
reads FITS data and returns DAP responses that are compatible with
DAP2 and the dap-server software.

%description -l pl.UTF-8
Ten pakiet zawiera moduł obsługujący dane FITS dla serwera danych
OPeNDAP. Odczytuje dane FITS i zwraca odpowiedzi DAP zgodne z
oprogramowaniem DAP2 i dap-server.

%prep
%setup -q -n fits_handler-%{version}

%build
# rebuild autotools for -as-needed to work
%{__libtoolize}
%{__aclocal} -I conf
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-cfits-include=%{_includedir} \
	--with-cfits-libdir=%{_libdir}
%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/bes/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYRIGHT ChangeLog NEWS README
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bes/modules/fits.conf
%attr(755,root,root) %{_libdir}/bes/libfits_module.so
%dir %{_datadir}/hyrax/data/fits
%{_datadir}/hyrax/data/fits/*.fts
