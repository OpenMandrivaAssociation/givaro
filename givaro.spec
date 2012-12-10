%define name		givaro
%define libgivaro	%mklibname %{name} 0
%define libgivaro_devel	%mklibname %{name} -d 

Name:		%{name}
Version:	3.7.0
Release:	2
Summary:	C++ library for arithmetic and algebraic computations
Group:		Sciences/Mathematics

License:	CeCILL-B
URL:		http://ljk.imag.fr/CASYS/LOGICIELS/givaro/
Source0:	https://forge.imag.fr/frs/download.php/207/%{name}-%{version}.tar.gz
Patch0:		givaro-config-script.patch
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
Group:		System/Libraries
Summary:	Givaro shared library


%description	-n %{libgivaro}
This package contains the givaro shared libraries.


%package	-n %{libgivaro_devel}
Group:		Development/C++
Summary:	Givaro development files
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib-%{name}-devel = %{version}-%{release}
Requires:	%{libgivaro} = %{version}-%{release}
Requires:	gmpxx-devel


%description	-n %{libgivaro_devel}
This package contains the givaro development files.


%prep
%setup -q -n givaro-%{version}
%patch0 -p0
%patch1 -p1

# Fix file encodings
for i in Licence_CeCILL-B_V1-fr.txt Licence_CeCILL-B_V1-en.txt;
do
	iconv -f  iso8859-1 -t utf-8 $i > $i.new && \
	touch -r $i $i.new && \
	mv $i.new $i
done

# Remove unnecessary executable bits
find examples -name Makefile.am -perm /0111 | xargs chmod a-x

%build
%configure2_5x --enable-shared --disable-static --enable-doc \
  --docdir=%{_docdir}/%{name}-devel-%{version}

# Fix an unused direct library dependency
sed -i 's/-lm -lgcc_s/-lgcc_s/' libtool

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
make check

%files		-n %{libgivaro}
%doc COPYRIGHT Licence_CeCILL-B_V1-en.txt Licence_CeCILL-B_V1-fr.txt
%{_libdir}/lib%{name}.so.*


%files		-n %{libgivaro_devel}
%doc docs/givaro-html docs/givaro-dev-html examples
%{_bindir}/%{name}-config
%{_includedir}/%{name}/
%{_includedir}/gmp++/
%{_datadir}/%{name}/
%{_includedir}/%{name}-config.h
%{_libdir}/lib%{name}.so


%changelog
* Mon Aug 13 2012 Paulo Andrade <pcpa@mandriva.com.br> 3.7.0-2
+ Revision: 814655
- Bump release and rebuild.
- Update to release matching http://pkgs.fedoraproject.org/cgit/givaro.git

* Wed Aug 08 2012 Paulo Andrade <pcpa@mandriva.com.br> 3.3.2-4
+ Revision: 812816
- Remove now bad libgmp-devel requires (#65714)

* Wed Dec 07 2011 Paulo Andrade <pcpa@mandriva.com.br> 3.3.2-3
+ Revision: 738705
- Rebuild for .la file removal.

* Mon Mar 14 2011 Paulo Andrade <pcpa@mandriva.com.br> 3.3.2-2
+ Revision: 644653
- Rebuild to ensure it is linked with proper libraries

* Wed Jul 14 2010 Paulo Andrade <pcpa@mandriva.com.br> 3.3.2-1mdv2011.0
+ Revision: 552983
- Update to version 3.3.2.

* Wed Feb 10 2010 Funda Wang <fwang@mandriva.org> 3.3.1-2mdv2010.1
+ Revision: 503613
- rebuild for new gmp

* Sat Jan 02 2010 Frederik Himpe <fhimpe@mandriva.org> 3.3.1-1mdv2010.1
+ Revision: 485096
- Update to new version 3.3.1

* Fri May 29 2009 Paulo Andrade <pcpa@mandriva.com.br> 3.2-5mdv2010.0
+ Revision: 381161
- Add libgmpxx-devel as build requires, what should remove the requirement
  of a "hack" patch in the linbox package (that ended being the reason of
  a major problem in the sagemath package, as reported by a cooker user).

* Fri May 22 2009 Paulo Andrade <pcpa@mandriva.com.br> 3.2-4mdv2010.0
+ Revision: 378828
+ rebuild (emptylog)

* Fri Apr 03 2009 Paulo Andrade <pcpa@mandriva.com.br> 3.2-3mdv2009.1
+ Revision: 363945
+ rebuild (emptylog)

* Fri Apr 03 2009 Paulo Andrade <pcpa@mandriva.com.br> 3.2-2mdv2009.1
+ Revision: 363922
- Build shared libraries, and properly name packages to libgivaro and
  libgivaro-devel.

* Fri Feb 27 2009 Paulo Andrade <pcpa@mandriva.com.br> 3.2-1mdv2009.1
+ Revision: 345802
- Initial import of givaro, version 3.2 (patchlevel 13).
  Givaro is a C++ library for arithmetic and algebraic computations.
- givaro

