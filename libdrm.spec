Summary: Digital Rights Managment library
Name: libdrm
Version: 1.0.3
Release: 1
License: MIT/X11
Group: System Environment/Libraries
URL: http://www.x.org
# No .bz2 avail upstream
Source0: http://dri.freedesktop.org/libdrm/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

#BuildRequires: xorg-x11-proto-devel
#BuildRequires: xorg-x11-xtrans-devel

#Provides: %{name}
Conflicts: XFree86-libs, xorg-x11-libs

%description
Digital Rights Management runtime library

%package devel
Summary: libdrm-devel
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

#Provides: %{name}-devel
Conflicts: XFree86-devel, xorg-x11-devel

%description devel
Digital Rights Management development package

%prep
%setup -q 

%build
# NOTE: We don't want to ship static libs.
%configure --disable-static
make

%install
rm -rf $RPM_BUILD_ROOT
# FIXME: makeinstall doesn't work due to upstream bug
#%%makeinstall DESTDIR=$RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc
%{_libdir}/libdrm.so.1
%{_libdir}/libdrm.so.1.0.0

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}
%dir %{_includedir}/drm
# NOTE: Headers are listed explicitly, so we can monitor additions/removals.
%{_includedir}/drm/drm.h
%{_includedir}/drm/drm_sarea.h
%{_includedir}/drm/i915_drm.h
%{_includedir}/drm/i915_drv.h
%{_includedir}/drm/imagine_drv.h
%{_includedir}/drm/mach64_drm.h
%{_includedir}/drm/mach64_drv.h
%{_includedir}/drm/mga_drm.h
%{_includedir}/drm/mga_drv.h
%{_includedir}/drm/mga_ucode.h
%{_includedir}/drm/r128_drm.h
%{_includedir}/drm/r128_drv.h
%{_includedir}/drm/r300_reg.h
%{_includedir}/drm/radeon_drm.h
%{_includedir}/drm/radeon_drv.h
%{_includedir}/drm/savage_drm.h
%{_includedir}/drm/savage_drv.h
%{_includedir}/drm/sis_drm.h
%{_includedir}/drm/sis_drv.h
%{_includedir}/drm/sis_ds.h
%{_includedir}/drm/tdfx_drv.h
%{_includedir}/drm/via_3d_reg.h
%{_includedir}/drm/via_drm.h
%{_includedir}/drm/via_drv.h
%{_includedir}/drm/via_ds.h
%{_includedir}/drm/via_mm.h
%{_includedir}/drm/via_verifier.h
%{_includedir}/xf86drm.h
%dir %{_libdir}
# NOTE: We don't want to ship static libs.
#%{_libdir}/libdrm.a
%{_libdir}/libdrm.so
%dir %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/libdrm.pc

%changelog
* Sat Sep 3 2005 Mike A. Harris <mharris@redhat.com> 1.0.3-1
- Initial build.
