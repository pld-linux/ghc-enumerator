#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	enumerator
Summary:	Reliable, high-performance processing with left-fold enumerators
Summary(pl.UTF-8):	Wiarygodne, wysoko wydajne enumeratory fold left
Name:		ghc-%{pkgname}
Version:	0.4.20
Release:	1
License:	MIT
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/enumerator
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	69ab1712b13571dfcc7ae4f8a1dcb616
URL:		http://hackage.haskell.org/package/enumerator
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 4.0
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-bytestring >= 0.9
BuildRequires:	ghc-containers >= 0.1
BuildRequires:	ghc-text >= 0.7
BuildRequires:	ghc-transformers >= 0.2
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 4.0
BuildRequires:	ghc-base-prof < 5
BuildRequires:	ghc-bytestring-prof >= 0.9
BuildRequires:	ghc-containers-prof >= 0.1
BuildRequires:	ghc-text-prof >= 0.7
BuildRequires:	ghc-transformers-prof >= 0.2
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_releq	ghc
Requires:	ghc-base >= 4.0
Requires:	ghc-base < 5
Requires:	ghc-bytestring >= 0.9
Requires:	ghc-containers >= 0.1
Requires:	ghc-text >= 0.7
Requires:	ghc-transformers >= 0.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
This library contains an enumerator implementation for Haskell,
designed to be both simple and efficient.

%description -l pl.UTF-8
Ta biblioteka zawiera implementację enumeratorów dla Haskella,
zaprojektowaną z myślą o prostocie i wydajności.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC.
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 4.0
Requires:	ghc-base-prof < 5
Requires:	ghc-bytestring-prof >= 0.9
Requires:	ghc-containers-prof >= 0.1
Requires:	ghc-text-prof >= 0.7
Requires:	ghc-transformers-prof >= 0.2

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/HSenumerator-%{version}.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSenumerator-%{version}.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Enumerator
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Enumerator/*.hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSenumerator-%{version}_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Enumerator/*.p_hi
%endif
