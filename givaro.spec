%define name	givaro
%define libname	%mklibname %{name} 0
%define devname	%mklibname %{name} -d 

Name:		%{name}
Summary:	C++ library for arithmetic and algebraic computations
Version:	3.3.1
Release:	%mkrel 2
License:	GPL
Group:		Sciences/Mathematics
Source0:	http://ljk.imag.fr/CASYS/LOGICIELS/givaro/Downloads/%{name}-%{version}.tar.gz
URL:		http://www-lmc.imag.fr/CASYS/LOGICIELS/givaro

BuildRequires:	libgmpxx-devel

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
In the joint CNRS-INRIA / INPG-UJF project APACHE, Givaro is a C++ library
for arithmetic and algebraic computations.
Its main features are implementations of the basic arithmetic of many
mathematical entities: Primes fields, Extensions Fields, Finite Fields,
Finite Rings, Polynomials, Algebraic numbers, Arbitrary precision integers
and rationals (C++ wrappers over gmp) It also provides data-structures and
templated classes for the manipulation of basic algebraic objects, such as
vectors, matrices (dense, sparse, structured), univariate polynomials (and
therefore recursive multivariate).
It contains different program modules and is fully compatible with the
LinBox linear algebra library and the Athapascan environment, which permits
parallel programming.

%package	-n %{libname}
Group:		System/Libraries
Summary:	Givaro shared library

%description	-n %{libname}
This package contains the givaro shared libraries.

%package	-n %{devname}
Group:		Development/C++
Summary:	Givaro development files
Obsoletes:	%{name}-devel < 3.3
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	libgmp-devel

%description	-n %{devname}
This package contains the givaro development files.

%prep
%setup -q -n givaro-%{version}

%build
%configure2_5x --with-gmp=%{_prefix} --disable-static --enable-shared
%make

%install
%makeinstall_std

%clean
rm -rf %{buildroot}

%files		-n %{libname}
%defattr(-,root,root)
%{_libdir}/libgivaro.so.*

%files		-n %{devname}
%defattr(-,root,root)
%{_bindir}/givaro-*
%{_includedir}/givaro-config.h
%dir %{_includedir}/givaro
%{_includedir}/givaro/*
%dir %{_includedir}/gmp++
%{_includedir}/gmp++/*
%{_libdir}/libgivaro.la
%{_libdir}/libgivaro.so
