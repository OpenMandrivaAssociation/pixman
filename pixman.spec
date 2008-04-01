%define major 0
%define apiver 1
%define libname %mklibname %{name}- %{apiver} %{major}
%define develname %mklibname %{name}- -d %{apiver}

Name:		pixman
Summary:	A pixel manipulation library
Version:	0.10.0
Release:	%mkrel 1
License:	MIT
Group:		System/Libraries
URL:		http://gitweb.freedesktop.org/?p=pixman.git
Source:		http://xorg.freedesktop.org/releases/individual/lib/%{name}-%{version}.tar.bz2
Patch0:		pixman-visibility.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Pixel manipulation Library.

%package -n %{libname}
Summary:	Pixel manipulation library
Group:		System/Libraries

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
Provides:	lib%{name}-%{apiver}-devel = %version-%release

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
%defattr(0644,root,root,0755)
%doc TODO
%{_libdir}/*.so
%{_libdir}/*.*a
%{_includedir}/pixman-1/*.h
%{_libdir}/pkgconfig/*
