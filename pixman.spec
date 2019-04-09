%define apiver 1
%define major 0
%define libname %mklibname %{name} %{apiver} %{major}
%define devname %mklibname %{name} -d

# (tpg) enable PGO build
%bcond_without pgo

Summary:	A pixel manipulation library
Name:		pixman
Version:	0.38.2
Release:	1
License:	MIT
Group:		System/Libraries
Url:		http://gitweb.freedesktop.org/?p=pixman.git
Source0:	http://xorg.freedesktop.org/releases/individual/lib/%{name}-%{version}.tar.bz2
BuildRequires:	pkgconfig(libpng)
BuildRequires:	meson
BuildRequires:	ninja

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
Obsoletes:	%{mklibname %{name} -d -s} < 0.38.0-2
Provides:	%{mklibname %{name} -d -s} = 0.38.0-2

%description -n %{devname}
This package provides the necessary development libraries and include
files to allow you to develop with pixman.

%prep
%autosetup -p1

%build

%if %{with pgo}
CFLAGS_PGO="%{optflags} -fprofile-instr-generate"
CXXFLAGS_PGO="%{optflags} -fprofile-instr-generate"
FFLAGS_PGO="$CFLAGS_PGO"
FCFLAGS_PGO="$CFLAGS_PGO"
LDFLAGS_PGO="%{ldflags} -fprofile-instr-generate"
export LLVM_PROFILE_FILE=%{name}-%p.profile.d
export LD_LIBRARY_PATH="$(pwd)"
%define _vpath_builddir pgo
mkdir pgo
CFLAGS="${CFLAGS_PGO}" CXXFLAGS="${CXXFLAGS_PGO}" FFLAGS="${FFLAGS_PGO}" FCFLAGS="${FCFLAGS_PGO}" LDFLAGS="${LDFLAGS_PGO}" CC="%{__cc}" %meson \
    -Dgtk=disabled \
    -Dlibpng=enabled \
    -Dloongson-mmi=disabled \
    -Dvmx=disabled \
    -Darm-simd=disabled \
    -Dmips-dspr2=disabled \
%ifarch %{armx}
    -Dneon=enabled \
    -Diwmmxt=enabled \
    -Diwmmxt2=true \
%else
    -Dneon=disabled \
    -Diwmmxt=disabled \
    -Diwmmxt2=false \
%endif
%ifarch %{ix86} %{x86_64}
    -Dmmx=enabled \
%endif
%ifarch %{x86_64}
    -Dsse2=enabled \
    -Dssse3=enabled \
%endif
    -Dopenmp=enabled

%meson_test || :
llvm-profdata merge --output=%{name}.profile ./pgo/*.profile.d
rm -f *.profile.d
cd pgo
ninja clean
cd -
rm -rf pgo
%undefine _vpath_builddir
CFLAGS="%{optflags} -fprofile-instr-use=$(realpath %{name}.profile)" \
CXXFLAGS="%{optflags} -fprofile-instr-use=$(realpath %{name}.profile)" \
LDFLAGS="%{ldflags} -fprofile-instr-use=$(realpath %{name}.profile)" \
%endif
%meson -Dgtk=disabled \
    -Dlibpng=enabled \
    -Dloongson-mmi=disabled \
    -Dvmx=disabled \
    -Darm-simd=disabled \
    -Dmips-dspr2=disabled \
%ifarch %{armx}
    -Dneon=enabled \
    -Diwmmxt=enabled \
    -Diwmmxt2=true \
%else
    -Dneon=disabled \
    -Diwmmxt=disabled \
    -Diwmmxt2=false \
%endif
%ifarch %{ix86} %{x86_64}
    -Dmmx=enabled \
    -Dsse2=enabled \
    -Dssse3=enabled \
%endif
    -Dopenmp=enabled

%meson_build

%install
%meson_install

%files -n %{libname}
%{_libdir}/*%{apiver}.so.%{major}*

%files -n %{devname}
%doc README AUTHORS
%{_libdir}/*.so
%dir %{_includedir}/pixman-1
%{_includedir}/pixman-1/*.h
%{_libdir}/pkgconfig/*.pc
