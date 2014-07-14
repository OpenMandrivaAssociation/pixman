%define apiver 1
%define major 0
%define libname %mklibname %{name} %{apiver} %{major}
%define devname %mklibname %{name} -d

Summary:	A pixel manipulation library
Name:		pixman
Version:	0.32.6
Release:	1
License:	MIT
Group:		System/Libraries
Url:		http://gitweb.freedesktop.org/?p=pixman.git
Source0:	http://xorg.freedesktop.org/releases/individual/lib/%{name}-%{version}.tar.bz2

%track
prog %name = {
	url = http://cairographics.org/releases/
	version = %version
	regex = pixman-(__VER__)\.tar\.bz2
}

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

%package -n %{devname}
Summary:	Libraries and include files for developing with libpixman
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}pixman-1-devel < 0.22.0

%description -n %{devname}
This package provides the necessary development libraries and include
files to allow you to develop with pixman.

%prep
%setup -q

%build
%configure \
	--disable-static

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

