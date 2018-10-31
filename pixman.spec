%define apiver 1
%define major 0
%define libname %mklibname %{name} %{apiver} %{major}
%define devname %mklibname %{name} -d
%define staticname %mklibname %{name} -d -s

Summary:	A pixel manipulation library
Name:		pixman
Version:	0.34.0
Release:	5
License:	MIT
Group:		System/Libraries
Url:		http://gitweb.freedesktop.org/?p=pixman.git
Source0:	http://xorg.freedesktop.org/releases/individual/lib/%{name}-%{version}.tar.bz2
Patch0:		clang.patch

%description
Pixel manipulation Library.

%package -n %{libname}
Summary:	Pixel manipulation library
Group:		System/Libraries
Provides:	%{_lib}pixman-1_0 = 0.22.0
Obsoletes:	%{_lib}pixman-1_0 < 0.22.0

%description -n %{libname}
A library for manipulating pixel regions -- a set of Y-X banded
rectangles, image compositing using the Porter/Duff model
and implicit mask generation for geometric primitives including
trapezoids, triangles, and rectangles.

%package -n %{devname}
Summary:	Libraries and include files for developing with libpixman
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Obsoletes:	%{_lib}pixman-1-devel < 0.22.0

%description -n %{devname}
This package provides the necessary development libraries and include
files to allow you to develop with pixman.

%package -n %{staticname}
Summary:	Libraries and include files for developing with libpixman
Group:		Development/C
Requires:	%{devname} = %{EVRD}
Provides:	%{name}-static-devel = %{EVRD}

%description -n %{staticname}
This package provides the necessary development libraries
files to allow you to link statically with pixman.

%prep
%setup -q
%apply_patches

%build
%configure \
        --enable-static

%make

%install
%makeinstall_std

%files -n %{libname}
%{_libdir}/*%{apiver}.so.%{major}*

%files -n %{devname}
%doc README AUTHORS
%{_libdir}/*.so
%dir %{_includedir}/pixman-1
%{_includedir}/pixman-1/*.h
%{_libdir}/pkgconfig/*.pc

%files -n %{staticname}
%{_libdir}/*.a
