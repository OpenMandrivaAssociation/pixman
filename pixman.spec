%define major 0
%define apiver 1
%define libname %mklibname %{name}-%{apiver} %{major}
%define develname %mklibname %{name} -d

Name:		pixman
Summary:	A pixel manipulation library
Version:	0.9.4
Release:	%mkrel 1
License:	MIT
Group:		System/Libraries
URL:		http://xorg.freedesktop.org/
Source:		http://xorg.freedesktop.org/releases/individual/lib/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Pixel manipulation Library.

%package -n %{libname}
Summary:	Pixel manipulation library
Group:		System/Libraries
Obsoletes:	%mklibname pixman 1

%description -n %{libname}
A library for manipulating pixel regions -- a set of Y-X banded
rectangles, image compositing using the Porter/Duff model
and implicit mask generation for geometric primitives including
trapezoids, triangles, and rectangles.
    
%package -n %{develname}
Summary:	Libraries and include files for developing with libpixman
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	slim-devel
Obsoletes:	slim-devel 
Obsoletes:	%mklibname pixman 1 -d
Provides:	%mklibname pixman 1 -d

%description -n %{develname}
This package provides the necessary development libraries and include
files to allow you to develop with pixman.

%prep
%setup -q

%build
%configure2_5x
%make

%install
rm -rf %{buildroot}

%makeinstall_std

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*%{apiver}.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%doc TODO
%{_libdir}/*.so
%{_libdir}/*.*a
%{_includedir}/*
%{_libdir}/pkgconfig/*
