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

%ifarch %{armx}
#(tpg) https://gitlab.freedesktop.org/pixman/pixman/-/issues/46
%global optflags %{optflags} -O3 -fno-integrated-as
%else
%global optflags %{optflags} -O3
%endif

Summary:	A pixel manipulation library
Name:		pixman
Version:	0.40.0
Release:	6
License:	MIT
Group:		System/Libraries
Url:		http://gitweb.freedesktop.org/?p=pixman.git
Source0:	http://xorg.freedesktop.org/releases/individual/lib/%{name}-%{version}.tar.xz
# (tpg) patches form upstream
Patch0:		0000-Prevent-empty-top-level-declaration.patch
Patch1:		0001-Add-ftrapping-math-to-default-cflags.patch
# (tpg) enable SIMD accelerations for pixman on aarch64
Patch2:		0000-added-aarch64-bilinear-implementations-ver.4.1.patch

BuildRequires:	meson
BuildRequires:	pkgconfig(zlib)
%if %{with pgo}
BuildRequires:	pkgconfig(libpng)
BuildRequires:	gomp-devel
%endif
%if %{with compat32}
BuildRequires:	devel(libz)
%endif

%description
The pixel-manipulation library for X and cairo.

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
%if %{with compat32}
%meson32 \
    -Dgtk=disabled \
    -Dlibpng=disabled \
    -Dloongson-mmi=disabled \
    -Dneon=disabled \
    -Diwmmxt=disabled \
    -Diwmmxt2=false \
    -Dvmx=disabled \
    -Darm-simd=disabled \
    -Dmips-dspr2=disabled \
    -Da64-neon=disabled \
    -Dmmx=enabled \
    -Dsse2=enabled \
    -Dssse3=enabled \
    -Dopenmp=disabled

%ninja_build -C build32
%endif

%if %{with pgo}
export LD_LIBRARY_PATH="$(pwd)"
%define _vpath_builddir pgo
mkdir pgo

CFLAGS="%{optflags} -fprofile-generate" \
CXXFLAGS="%{optflags} -fprofile-generate" \
LDFLAGS="%{build_ldflags} -fprofile-generate" \
CC="%{__cc}" \
%meson \
    -Dgtk=disabled \
    -Dlibpng=enabled \
    -Dloongson-mmi=disabled \
    -Dvmx=disabled \
    -Darm-simd=disabled \
    -Dmips-dspr2=disabled \
    -Diwmmxt=disabled \
    -Diwmmxt2=false \
%ifarch %{arm}
    -Dneon=enabled \
    -Dgnu-inline-asm=enabled \
%else
    -Dneon=disabled \
%endif
%ifarch aarch64
    -Da64-neon=enabled \
%else
    -Da64-neon=disabled \
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
    -Dopenmp=enabled

%meson_test || :
llvm-profdata merge --output=%{name}-llvm.profdata $(find ./pgo -name "*.profraw" -type f)
PROFDATA="$(realpath %{name}-llvm.profdata)"
rm -f pgo/*.profraw
cd pgo
ninja clean
cd -
rm -rf pgo
%undefine _vpath_builddir

CFLAGS="%{optflags} -fprofile-use=$PROFDATA" \
CXXFLAGS="%{optflags} -fprofile-use=$PROFDATA" \
LDFLAGS="%{build_ldflags} -fprofile-use=$PROFDATA" \
%endif
%meson \
    -Dgtk=disabled \
    -Dlibpng=disabled \
    -Dloongson-mmi=disabled \
    -Dvmx=disabled \
    -Darm-simd=disabled \
    -Dmips-dspr2=disabled \
    -Diwmmxt=disabled \
    -Diwmmxt2=false \
%ifarch %{arm}
    -Dneon=enabled \
    -Dgnu-inline-asm=enabled \
%else
    -Dneon=disabled \
%endif
%ifarch aarch64
    -Da64-neon=enabled \
%else
    -Da64-neon=disabled \
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
    -Dopenmp=disabled

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
