# pixman is used by various wine dependencies
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

%define apiver 1
%define major 0
%define libname %mklibname %{name} %{apiver} %{major}
%define devname %mklibname %{name} -d
%define lib32name %mklib32name %{name} %{apiver} %{major}
%define dev32name %mklib32name %{name} -d

# (tpg) enable PGO build
%bcond_without pgo

%ifarch armv7hnl
%global optflags %{optflags} -fno-integrated-as
%endif

Summary:	A pixel manipulation library
Name:		pixman
Version:	0.40.0
Release:	2
License:	MIT
Group:		System/Libraries
Url:		http://gitweb.freedesktop.org/?p=pixman.git
Source0:	http://xorg.freedesktop.org/releases/individual/lib/%{name}-%{version}.tar.xz
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(zlib)
# remove me in future
%ifarch riscv64
BuildRequires:	gomp-devel
%endif
BuildRequires:	meson
BuildRequires:	ninja
%if %{with compat32}
BuildRequires:	devel(libpng16)
BuildRequires:	devel(libz)
BuildRequires:	libgomp-devel
%endif

%description
Pixel manipulation Library.

%package -n %{libname}
Summary:	Pixel manipulation library
Group:		System/Libraries
Provides:	%{_lib}pixman-1_0 = %{EVRD}
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
Provides:	%{mklibname %{name} -d -s} = %{EVRD}

%description -n %{devname}
This package provides the necessary development libraries and include
files to allow you to develop with pixman.

%if %{with compat32}
%package -n %{lib32name}
Summary:	Pixel manipulation library (32-bit)
Group:		System/Libraries

%description -n %{lib32name}
A library for manipulating pixel regions -- a set of Y-X banded
rectangles, image compositing using the Porter/Duff model
and implicit mask generation for geometric primitives including
trapezoids, triangles, and rectangles.

%package -n %{dev32name}
Summary:	Libraries and include files for developing with libpixman (32-bit)
Group:		Development/C
Requires:	%{devname} = %{EVRD}
Requires:	%{lib32name} = %{EVRD}

%description -n %{dev32name}
This package provides the necessary development libraries and include
files to allow you to develop with pixman.
%endif

%prep
%autosetup -p1

%build
export CONFIGURE_TOP="$(pwd)"
%if %{with compat32}
%meson32 \
    -Dgtk=disabled \
    -Dlibpng=enabled \
    -Dloongson-mmi=disabled \
    -Dneon=disabled \
    -Diwmmxt=disabled \
    -Diwmmxt2=false \
    -Dvmx=disabled \
    -Darm-simd=disabled \
    -Dmips-dspr2=disabled \
    -Dmmx=enabled \
    -Dsse2=enabled \
    -Dssse3=enabled \
    -Dopenmp=enabled
%ninja_build -C build32
%endif

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
%ifarch %{arm}
    -Dneon=enabled \
    -Diwmmxt=disabled \
    -Diwmmxt2=false \
    -Dgnu-inline-asm=enabled \
%else
    -Dneon=disabled \
    -Diwmmxt=disabled \
    -Diwmmxt2=false \
%endif
%ifarch %{ix86} %{x86_64}
    -Dmmx=enabled \
%else
    -Dmmx=disabled \
%endif
%ifarch %{x86_64}
    -Dsse2=enabled \
    -Dssse3=enabled \
%else
    -Dsse2=disabled \
    -Dssse3=disabled \
%endif
%ifarch riscv64
    -Dopenmp=disabled
%else
    -Dopenmp=enabled
%endif


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
%ifarch %{arm}
    -Dneon=enabled \
    -Diwmmxt=disabled \
    -Diwmmxt2=false \
    -Dgnu-inline-asm=enabled \
%else
    -Dneon=disabled \
    -Diwmmxt=disabled \
    -Diwmmxt2=false \
%endif
%ifarch %{ix86} %{x86_64}
    -Dmmx=enabled \
    -Dsse2=enabled \
    -Dssse3=enabled \
%else
    -Dmmx=disabled \
    -Dsse2=disabled \
    -Dssse3=disabled \
%endif
%ifarch riscv64
    -Dopenmp=disabled
%else
    -Dopenmp=enabled
%endif

%meson_build

%install
%if %{with compat32}
%ninja_install -C build32
%endif
%meson_install

%files -n %{libname}
%{_libdir}/*%{apiver}.so.%{major}*

%files -n %{devname}
%doc README AUTHORS
%{_libdir}/*.so
%dir %{_includedir}/pixman-1
%{_includedir}/pixman-1/*.h
%{_libdir}/pkgconfig/*.pc

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/*%{apiver}.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/*.so
%{_prefix}/lib/pkgconfig/*.pc
%endif
