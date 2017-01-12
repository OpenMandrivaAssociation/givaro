%define major	9
%define libgivaro	%mklibname %{name} %{major}
%define libgivaro_devel	%mklibname %{name} -d 
%define _disable_lto 1

Name:		givaro
Version:	4.0.2
Release:	1
Summary:	C++ library for arithmetic and algebraic computations
License:	CeCILL-B
URL:		http://givaro.forge.imag.fr/
Source0:	https://github.com/linbox-team/%{name}/releases/download/v%{version}/givaro-%{version}.tar.gz
Patch1:		givaro-underlink.patch

BuildRequires:	doxygen
BuildRequires:	gmpxx-devel
BuildRequires:	texlive


%description
Givaro is a C++ library for arithmetic and algebraic computations.
Its main features are implementations of the basic arithmetic of many
mathematical entities: Primes fields, Extensions Fields, Finite Fields,
Finite Rings, Polynomials, Algebraic numbers, Arbitrary precision
integers and rationals (C++ wrappers over gmp) It also provides
data-structures and templated classes for the manipulation of basic
algebraic objects, such as vectors, matrices (dense, sparse, structured),
univariate polynomials (and therefore recursive multivariate).


%package	-n %{libgivaro}
Summary:	Givaro shared library


%description	-n %{libgivaro}
This package contains the givaro shared libraries.


%package	-n %{libgivaro_devel}
Summary:	Givaro development files
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib-%{name}-devel = %{version}-%{release}
Requires:	%{libgivaro} = %{version}-%{release}
Requires:	gmpxx-devel


%description	-n %{libgivaro_devel}
This package contains the givaro development files.


%prep
%setup -q -n givaro-%{version}

# Fix file encodings
for i in Licence_CeCILL-B_V1-fr.txt Licence_CeCILL-B_V1-en.txt COPYING AUTHORS;
do
	iconv -f  iso8859-1 -t utf-8 $i > $i.new && \
	touch -r $i $i.new && \
	mv $i.new $i
done

# Remove unnecessary executable bits
find examples -name Makefile.am -perm /0111 | xargs chmod a-x

%build
export CC=gcc
export CXX=g++
%configure2_5x --enable-shared --disable-static --enable-doc \
  --docdir=%{_docdir}/%{name}-devel-%{version} CPPFLAGS="-D__int64=__int64_t"

# Get rid of undesirable hardcoded rpaths, and workaround libtool reordering
# -Wl,--as-needed after all the libraries.
sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    -e 's|^LTCC="gcc"|LTCC="gcc -Wl,--as-needed"|' \
    -e 's|^CC="\(g..\)"|CC="\1 -Wl,--as-needed"|' \
    -i libtool

make %{?_smp_mflags}

# We don't want these files with the doxygen-generated files
rm -f docs/givaro-html/{AUTHORS,COPYING,INSTALL}


%install
# Documentation installation is hopelessly broken
sed -i 's/^SUBDIRS =.*/SUBDIRS = src macros tests/' Makefile

make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib%{name}.la

#givaro-makefile is installed incorrectly in usr/bin
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
mv $RPM_BUILD_ROOT/%{_bindir}/givaro-makefile $RPM_BUILD_ROOT%{_datadir}/%{name}
chmod 644  $RPM_BUILD_ROOT%{_datadir}/%{name}/givaro-makefile
sed -i '\%#! /bin/sh%D' $RPM_BUILD_ROOT%{_datadir}/%{name}/givaro-makefile


%check
LD_LIBRARY_PATH=$PWD/src/.libs: make check

%files		-n %{libgivaro}
%doc AUTHORS COPYRIGHT COPYING
%doc Licence_CeCILL-B_V1-en.txt Licence_CeCILL-B_V1-fr.txt
%{_libdir}/lib%{name}.so.%{major}*


%files		-n %{libgivaro_devel}
%doc docs/givaro-html docs/givaro-dev-html examples
%{_bindir}/%{name}-config
%{_includedir}/%{name}/
%{_includedir}/gmp++/
%{_includedir}/recint
%{_datadir}/%{name}/
%{_includedir}/%{name}-config.h
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
