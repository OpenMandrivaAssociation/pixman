%define major 0
%define apiver 1
%define libname %mklibname %{name} %{apiver} %{major}
%define develname %mklibname %{name} -d

Summary:	A pixel manipulation library
Name:		pixman
Version:	0.27.2
Release:	1
License:	MIT
Group:		System/Libraries
URL:		http://gitweb.freedesktop.org/?p=pixman.git
Source0:	http://xorg.freedesktop.org/releases/individual/lib/%{name}-%{version}.tar.bz2

%description
Pixel manipulation Library.

%package -n %{libname}
Summary:	Pixel manipulation library
Group:		System/Libraries
Provides:	%{_lib}pixman-1_0
Obsoletes:	%{_lib}pixman-1_0 < 0.22.0

%description -n %{libname}
A library for manipulating pixel regions -- a set of Y-X banded
rectangles, image compositing using the Porter/Duff model
and implicit mask generation for geometric primitives including
trapezoids, triangles, and rectangles.

%package -n %{develname}
Summary:	Libraries and include files for developing with libpixman
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-%{apiver}-devel = %{version}-%{release}
Obsoletes:	%{_lib}pixman-1-devel < 0.22.0

%description -n %{develname}
This package provides the necessary development libraries and include
files to allow you to develop with pixman.

%prep
%setup -q

%build
%configure2_5x \
	--disable-static
%make

%install
%makeinstall_std

%files -n %{libname}
%{_libdir}/*%{apiver}.so.%{major}*

%files -n %{develname}
%doc TODO
%{_libdir}/*.so
%{_includedir}/pixman-1/*.h
%{_libdir}/pkgconfig/*.pc
