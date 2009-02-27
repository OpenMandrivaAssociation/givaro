Name:		givaro-devel
Summary:	C++ library for arithmetic and algebraic computations
Version:	3.2
Release:	%mkrel 1
License:	GPL
Source0:	http://www-lmc.imag.fr/CASYS/LOGICIELS/givaro/Downloads/givaro-3.2.tar.gz
URL:		http://www-lmc.imag.fr/CASYS/LOGICIELS/givaro

BuildRequires:	libgmp-devel
Requires:	libgmp-devel

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

%prep
%setup -q -n givaro-%{version}.13

%build
%configure2_5x --with-gmp=%{_prefix}
%make

%install
%makeinstall_std

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/givaro-*
%{_includedir}/givaro-config.h
%dir %{_includedir}/givaro
%{_includedir}/givaro/*
%dir %{_includedir}/gmp++
%{_includedir}/gmp++/*
%{_libdir}/libgivaro.*
