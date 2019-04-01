%define apiver 1
%define major 0
%define libname %mklibname %{name} %{apiver} %{major}
%define devname %mklibname %{name} -d
%define staticname %mklibname %{name} -d -s

# (tpg) enable PGO build
%bcond_without pgo

Summary:	A pixel manipulation library
Name:		pixman
Version:	0.38.0
Release:	2
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
    -Dsse3=enabled \
%endif
    -Dopenmp=enabled

%meson_test || :
llvm-profdata merge --output=%{name}.profile ./build/*.profile.d
unset LLVM_PROFILE_FILE
unset LD_LIBRARY_PATH
rm -f *.profile.d
cd build
ninja clean
cd -
rm -rf build

CFLAGS="%{optflags} -fprofile-instr-use=$(realpath %{name}.profile)" \
CXXFLAGS="%{optflags} -fprofile-instr-use=$(realpath %{name}.profile)" \
LDFLAGS="%{ldflags} -fprofile-use" \
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
    -Dsse3=enabled \
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

%files -n %{staticname}
%{_libdir}/*.a
