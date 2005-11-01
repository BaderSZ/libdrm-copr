Summary: Digital Rights Managment library
Name: libdrm
Version: 1.0.5
Release: 1
License: MIT/X11
Group: System Environment/Libraries
URL: http://dri.sourceforge.net
# No .bz2 avail upstream
Source0: http://dri.freedesktop.org/libdrm/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#BuildRequires: xorg-x11-proto-devel
#BuildRequires: xorg-x11-xtrans-devel

BuildRequires: pkgconfig
BuildRequires: libX11-devel

Conflicts: XFree86-libs, xorg-x11-libs

%description
Digital Rights Management runtime library

%package devel
Summary: libdrm-devel
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

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
%doc README
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
%{_includedir}/drm/mach64_drm.h
%{_includedir}/drm/mga_drm.h
%{_includedir}/drm/r128_drm.h
%{_includedir}/drm/r300_reg.h
%{_includedir}/drm/radeon_drm.h
%{_includedir}/drm/savage_drm.h
%{_includedir}/drm/sis_drm.h
%{_includedir}/drm/via_3d_reg.h
%{_includedir}/drm/via_drm.h
%{_includedir}/xf86drm.h
%dir %{_libdir}
# NOTE: We don't want to ship static libs.
#%{_libdir}/libdrm.a
%{_libdir}/libdrm.so
%dir %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/libdrm.pc

%changelog
* Tue Nov  1 2005 Mike A. Harris <mharris@redhat.com> 1.0.5-1
- Updated libdrm to version 1.0.5 from dri.sf.net upstream to work around
  mesa unichrome dri driver compile failure.

* Mon Oct 24 2005 Mike A. Harris <mharris@redhat.com> 1.0.4-1
- Updated libdrm to version 1.0.4 from X11R7 RC1
- Remove i915_drv.h, imagine_drv.h, mach64_drv.h, mga_drv.h, mga_ucode.h,
  r128_drv.h, radeon_drv.h, savage_drv.h, sis_drv.h, sis_ds.h, tdfx_drv.h,
  via_drv.h, via_ds.h, via_mm.h, via_verifier.h from file manifest.

* Tue Oct 4 2005 Mike A. Harris <mharris@redhat.com> 1.0.3-3
- Update BuildRoot to use Fedora Packaging Guidelines.
- Add missing "BuildRequires: libX11-devel, pkgconfig"

* Thu Sep 29 2005 Mike A. Harris <mharris@redhat.com> 1.0.3-2
- Add missing documentation to doc macro
- Fix spec file project URL

* Sat Sep 3 2005 Mike A. Harris <mharris@redhat.com> 1.0.3-1
- Initial build.
