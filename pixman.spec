%define major 0
%define apiver 1
%define libname %mklibname %{name} %{apiver} %{major}
%define develname %mklibname %{name} -d

Summary:	A pixel manipulation library
Name:		pixman
Version:	0.30.0
Release:	1
License:	MIT
Group:		System/Libraries
URL:		http://gitweb.freedesktop.org/?p=pixman.git
Source0:	http://xorg.freedesktop.org/releases/individual/lib/%{name}-%{version}.tar.bz2
Patch0:		pixman-aarch64.patch

%track
prog %name = {
	url = http://cairographics.org/releases/
	version = %version
	regex = pixman-(__VER__)\.tar\.gz
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
%patch0 -p1

%build
%configure2_5x \
	--disable-static
%make

%install
%makeinstall_std

%files -n %{libname}
%{_libdir}/*%{apiver}.so.%{major}*

%files -n %{develname}
%doc README AUTHORS
%{_libdir}/*.so
%dir %{_includedir}/pixman-1
%{_includedir}/pixman-1/*.h
%{_libdir}/pkgconfig/*.pc


%changelog
* Sat Oct 27 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 0.27.4-1
+ Revision: 820034
- fix docs
- update to new version 0.27.4

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - own %%{_includedir}/pixman-1

* Tue Aug 07 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 0.27.2-1
+ Revision: 812234
- update to new version 0.27.2

* Sun Jul 01 2012 Bernhard Rosenkraenzer <bero@bero.eu> 0.26.2-1
+ Revision: 807698
- Update to 0.26.2

* Mon May 28 2012 Alexander Khrukin <akhrukin@mandriva.org> 0.26.0-1
+ Revision: 800982
- version update 0.26.0

* Mon May 21 2012 Bernhard Rosenkraenzer <bero@bero.eu> 0.25.6-1
+ Revision: 799745
- Update to 0.25.6

* Thu Mar 29 2012 Bernhard Rosenkraenzer <bero@bero.eu> 0.25.2-1
+ Revision: 788250
- Update to 0.25.2

* Sun Feb 19 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 0.24.4-1
+ Revision: 777326
- update to new version 0.24.4

* Wed Feb 01 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 0.24.2-1
+ Revision: 770547
- update to new version 0.24.2

* Wed Dec 28 2011 Matthew Dawkins <mattydaw@mandriva.org> 0.24.0-2
+ Revision: 745857
- bump release
- rebuild
- removed .la files
- cleaned up spec

* Wed Nov 09 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 0.24.0-1
+ Revision: 729378
- update to new version 0.24.0

* Sat Sep 03 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 0.22.2-1
+ Revision: 698106
- update to new version 0.22.2

  + Matthew Dawkins <mattydaw@mandriva.org>
    - added a provides for old libname
    - disabled static build

* Wed May 04 2011 Funda Wang <fwang@mandriva.org> 0.22.0-1
+ Revision: 666172
- new version 0.22.0

* Fri Apr 22 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 0.20.2-2
+ Revision: 656746
- rebuild for missing ix68 packages (mdvbz#63101)

* Wed Jan 26 2011 Thierry Vignaud <tv@mandriva.org> 0.20.2-1
+ Revision: 632908
- new release

* Thu Oct 28 2010 Thierry Vignaud <tv@mandriva.org> 0.20.0-1mdv2011.0
+ Revision: 589753
- new release

* Thu Oct 21 2010 Thierry Vignaud <tv@mandriva.org> 0.19.6-1mdv2011.0
+ Revision: 587062
- new release

* Tue Sep 21 2010 Thierry Vignaud <tv@mandriva.org> 0.19.4-1mdv2011.0
+ Revision: 580432
- new release

* Mon Aug 23 2010 Thierry Vignaud <tv@mandriva.org> 0.19.2-1mdv2011.0
+ Revision: 572375
- new release

* Tue Aug 17 2010 Thierry Vignaud <tv@mandriva.org> 0.18.4-1mdv2011.0
+ Revision: 571085
- new release

* Mon May 17 2010 Frederic Crozat <fcrozat@mandriva.com> 0.18.2-1mdv2010.1
+ Revision: 544922
- Release 0.18.2

* Thu Apr 01 2010 Christophe Fergeau <cfergeau@mandriva.com> 0.18.0-1mdv2010.1
+ Revision: 530627
- pixman 0.18.0

* Wed Mar 24 2010 Christophe Fergeau <cfergeau@mandriva.com> 0.17.14-1mdv2010.1
+ Revision: 527082
- pixman 0.17.14

* Thu Mar 18 2010 Frederic Crozat <fcrozat@mandriva.com> 0.17.12-1mdv2010.1
+ Revision: 524912
- Release 0.17.12

* Mon Mar 08 2010 Christophe Fergeau <cfergeau@mandriva.com> 0.17.10-1mdv2010.1
+ Revision: 515806
- new upstream release: 0.17.10

* Thu Feb 25 2010 Frederic Crozat <fcrozat@mandriva.com> 0.17.8-1mdv2010.1
+ Revision: 510935
- Release 0.17.8
 -Remove patch0 (not applied anymore)

* Mon Feb 15 2010 Christophe Fergeau <cfergeau@mandriva.com> 0.17.6-1mdv2010.1
+ Revision: 506138
- pixman 0.17.6

* Thu Feb 11 2010 Christophe Fergeau <cfergeau@mandriva.com> 0.17.4-1mdv2010.1
+ Revision: 504236
- pixman 0.17.4

* Fri Nov 20 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 0.17.2-1mdv2010.1
+ Revision: 467733
- update to new version 0.17.2

* Mon Sep 28 2009 Frederik Himpe <fhimpe@mandriva.org> 0.16.2-1mdv2010.0
+ Revision: 450626
- update to new version 0.16.2

* Sun Aug 30 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 0.16.0-1mdv2010.0
+ Revision: 422500
- update to new version 0.16.0

* Wed Aug 12 2009 Frederic Crozat <fcrozat@mandriva.com> 0.15.20-1mdv2010.0
+ Revision: 415372
- Release 0.15.20

* Tue Jul 21 2009 Thierry Vignaud <tv@mandriva.org> 0.15.18-1mdv2010.0
+ Revision: 398429
- new release (should fix fdo #22484 and thus mdv #52320)

* Sat Jul 18 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 0.15.16-1mdv2010.0
+ Revision: 397061
- update to new version 0.15.16

* Fri Jun 26 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 0.15.14-1mdv2010.0
+ Revision: 389283
- update to new version 0.15.14

* Wed Jun 17 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 0.15.12-1mdv2010.0
+ Revision: 386833
- update to new version 0.15.12

* Sun Jun 07 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 0.15.10-1mdv2010.0
+ Revision: 383551
- update to new version 0.15.10

* Mon Jun 01 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 0.15.8-1mdv2010.0
+ Revision: 381999
- update to new version 0.15.8

* Sat May 30 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 0.15.6-1mdv2010.0
+ Revision: 381322
- update to new version 0.15.6

* Sat Feb 07 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 0.14.0-1mdv2009.1
+ Revision: 338320
- update to new version 0.14.0

* Sun Nov 30 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 0.13.2-1mdv2009.1
+ Revision: 308557
- update to new version 0.13.2

* Thu Sep 18 2008 Götz Waschk <waschk@mandriva.org> 0.12.0-1mdv2009.0
+ Revision: 285592
- new version
- drop patch 1

* Fri Sep 12 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 0.11.10-1mdv2009.0
+ Revision: 283968
- update to new version 0.11.10
- Patch1: do not render weird artifacts (fd.o bug #17477) (hopefully this will fix also mdv bug #39971 ?)

* Tue Aug 12 2008 Götz Waschk <waschk@mandriva.org> 0.11.8-1mdv2009.0
+ Revision: 271004
- new version

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 0.10.0-2mdv2009.0
+ Revision: 224920
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Tue Apr 01 2008 Frederic Crozat <fcrozat@mandriva.com> 0.10.0-1mdv2008.1
+ Revision: 191349
- Release 0.10.0 (needed for cairo 1.6.0 when released), with additional MMX optimisations as a bonus

* Tue Jan 15 2008 Paulo Andrade <pcpa@mandriva.com.br> 0.9.6-2mdv2008.1
+ Revision: 152909
- Disable patch0 as it was used only to "document" functions called by
  the X Server.
- Still a noop patch, but add an explicit _X_EXPORT for other symbols. This
  time symbols used by some X Server modules.
- This is a "noop" patch. But it can be considered a list of the functions,
  code from X Server uses from pixmap (libpixman-1), at a later stage, this
  library can be changed to make available only the public symbols.

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Oct 25 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 0.9.6-1mdv2008.1
+ Revision: 102081
- new version

* Tue Oct 16 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 0.9.5-3mdv2008.1
+ Revision: 99035
+ rebuild (emptylog)

* Wed Oct 10 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 0.9.5-1mdv2008.1
+ Revision: 96931
- new upstream version: 0.9.5
- minor spec cleanup

  + Götz Waschk <waschk@mandriva.org>
    - fix library name to be compatible with libpixman in main
    - remove wrong obsoletes

* Tue Aug 07 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 0.9.4-1mdv2008.0
+ Revision: 59882
- Import pixman

