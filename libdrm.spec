%define gitdate 20080814

Summary: Direct Rendering Manager runtime library
Name: libdrm
Version: 2.4.0
Release: 0.20%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://dri.sourceforge.net
#Source0: http://dri.freedesktop.org/libdrm/%{name}-%{version}.tar.bz2
Source0: %{name}-%{gitdate}.tar.bz2
Source1: make-git-snapshot.sh
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: pkgconfig automake autoconf libtool

BuildRequires: kernel-headers >= 2.6.27-0.317.rc5.git10.fc10

Source2: 91-drm-modeset.rules
Source3: i915modeset

#Patch1: libdrm-modesetting.patch
Patch2: libdrm-2.4.0-no-freaking-mknod.patch
# udev vs pam.console vs hal vs xml vs ConsoleKit
# - funk that just bash it direct for now -
Patch3: libdrm-make-dri-perms-okay.patch
Patch4: libdrm-2.4.0-no-bc.patch
Patch5: libdrm-wait-udev.patch
Patch6: libdrm-gtt-map-support-3.patch

%description
Direct Rendering Manager runtime library

%package devel
Summary: Direct Rendering Manager development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: kernel-headers >= 2.6.27-0.144.rc0.git2.fc10

%description devel
Direct Rendering Manager development package

%prep
%setup -q -n %{name}-%{gitdate}
#patch2 -p1 -b .mknod
%patch3 -p1 -b .forceperms
%patch4 -p1 -b .no-bc
%patch5 -p1 -b .udev-wait
%patch6 -p1 -b .gttmap

%build
autoreconf -v --install || exit 1
%configure --enable-udev
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# SUBDIRS=libdrm
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/

# NOTE: We intentionally don't ship *.la files
find $RPM_BUILD_ROOT -type f -name '*.la' | xargs rm -f -- || :
find $RPM_BUILD_ROOT -type f -name '*_drm.h' | xargs rm -f -- || :
for i in drm.h drm_sarea.h r300_reg.h via_3d_reg.h
do
rm -f $RPM_BUILD_ROOT/usr/include/drm/$i
done

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README
%{_libdir}/libdrm.so.2
%{_libdir}/libdrm.so.2.3.0
%{_sysconfdir}/udev/rules.d/91-drm-modeset.rules
%{_sysconfdir}/modprobe.d/i915modeset

%files devel
%defattr(-,root,root,-)
# FIXME should be in drm/ too
%{_includedir}/xf86drm.h
%{_includedir}/xf86drmMode.h
%{_includedir}/dri_bufmgr.h
%{_includedir}/intel_bufmgr.h
%{_libdir}/libdrm.so
%{_libdir}/pkgconfig/libdrm.pc

%changelog
* Tue Sep 09 2008 Dave Airlie <airlied@redhat.com> 2.4.0-0.20
- add gtt mapping for intel modesetting

* Thu Aug 14 2008 Dave Airlie <airlied@redhat.com> 2.4.0-0.19
- add back modesetting support - this is a snapshot from modesetting-gem
- any bugs are in the other packages that fail to build

* Mon Aug 11 2008 Adam Jackson <ajax@redhat.com> 2.4.0-0.18
- Today's git snap.

* Sun Aug 10 2008 Dave Airlie <airlied@redhat.com> 2.4.0-0.17
- attempt to fix race with udev by just waiting for udev

* Fri Aug 01 2008 Dave Airlie <airlied@redhat.com> 2.4.0-0.16
- new libdrm snapshot with modesetting for radeon interfaces

* Thu Jul 17 2008 Kristian Høgsberg <krh@redhat.com> - 2.4.0-0.15
- Avoid shared-core when doing make install so we don't install kernel
  header files.  Drop kernel header files from -devel pkg files list.

* Thu Jul 17 2008 Dave Airlie <airlied@redhat.com> 2.4.0-0.14
- kernel headers now installs somes of these files for us

* Wed Jun 18 2008 Dave Airlie <airlied@redhat.com> 2.4.0-0.13
- add modeset ctl interface fix

* Wed May 28 2008 Dave Airlie <airlied@redhat.com> 2.4.0-0.12
- add r500 support patch

* Tue Apr 29 2008 Adam Jackson <ajax@redhat.com> 2.4.0-0.11
- libdrm-2.4.0-no-bc.patch: Delete the /proc/dri BC code.  It's not needed,
  and the kernel implementation is sufficiently broken that we should avoid
  ever touching it.

* Wed Mar 19 2008 Dave Airlie <airlied@redhat.com> 2.4.0-0.10
- force libdrm to make the node perms useful to everyone 

* Fri Mar 07 2008 Dave Airlie <airlied@redhat.com> 2.4.0-0.9
- add support for new sysfs structure

* Thu Mar 06 2008 Dave Airlie <airlied@redhat.com> 2.4.0-0.8
- add modprobe.d file so i915 modesetting can be specified on kernel command
  line

* Wed Mar 05 2008 Dave Airlie <airlied@redhat.com> 2.4.0-0.7
- add udev rules for modesetting nodes.

* Wed Mar 05 2008 Dave Airlie <airlied@redhat.com> 2.4.0-0.6
- add initial modesetting headers to the mix - this API isn't stable 

* Mon Mar  3 2008 Kristian Høgsberg <krh@redhat.com> - 2.4.0-0.5
- What he said.

* Fri Feb 15 2008 Adam Jackson <ajax@redhat.com> 2.4.0-0.4
- Today's git snapshot for updated headers.

* Mon Jan 21 2008 Adam Jackson <ajax@redhat.com> 2.4.0-0.3
- libdrm-2.4.0-no-freaking-mknod.patch: Disable.  Deep voodoo.

* Thu Nov 30 2007 Dave Airlie <airlied@redhat.com> - 2.4.0-0.2
- Update to a newer upstream snapshot

* Mon Nov 12 2007 Adam Jackson <ajax@redhat.com> 2.4.0-0.1
- libdrm-2.4.0-no-freaking-mknod.patch: Don't magically mknod the device
  file, that's what udev is for.

* Thu Nov 01 2007 Dave Airlie <airlied@redhat.com> - 2.4.0-0
- Import a snapshot of what will be 2.4 upstream

* Thu Sep 20 2007 Dave Airlie <airlied@redhat.com> - 2.3.0-7
- Update nouveau patch.

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 2.3.0-6
- Rebuild for build id

* Fri Mar 30 2007 Kristian Høgsberg <krh@redhat.com> - 2.3.0-5
- Update nouveau patch.

* Tue Feb 19 2007 Adam Jackson <ajax@redhat.com> 2.3.0-4
- Update nouveau patch
- Fix License tag and other rpmlint noise

* Fri Feb 02 2007 Adam Jackson <ajax@redhat.com> 2.3.0-3
- Remove ExclusiveArch.

* Mon Jan 29 2007 Adam Jackson <ajax@redhat.com> 2.3.0-2
- Change default device mode to 0666. (#221545)

* Fri Nov 17 2006 Adam Jackson <ajax@redhat.com> 2.3.0-1.fc7
- Update to 2.3.0 from upstream.
- Add nouveau userspace header.

* Wed Jul 26 2006 Kristian Høgsberg <krh@redhat.com> - 2.0.2-3.fc6
- Build for rawhide.

* Wed Jul 26 2006 Kristian Høgsberg <krh@redhat.com> - 2.0.2-2.fc5.aiglx
- Build for fc5 aiglx repo.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 2.0.2-2.1
- rebuild

* Tue Jun 27 2006 Adam Jackson <ajackson@redhat.com> 2.0.2-2
- Bump to 2.0.2 for header updates.  Fix BuildRequires.  Minor spec cleanups. 

* Mon Jun 09 2006 Mike A. Harris <mharris@redhat.com> 2.0.1-4
- Added "Exclusivearch: ix86, x86_64, ia64, ppc, alpha, sparc, sparc64" to
  restrict build to DRI-enabled architectures.

* Thu Jun 08 2006 Mike A. Harris <mharris@redhat.com> 2.0.1-3
- Remove package ownership of mandir/libdir/etc.

* Mon Apr 10 2006 Kristian Høgsberg <krh@redhat.com> 2.0.1-2
- Bump for fc5 build.

* Thu Mar 30 2006 Adam Jackson <ajackson@redhat.com> 2.0.1-1
- Bump to libdrm 2.0.1 from upstream.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 2.0-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 2.0-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 11 2006 Mike A. Harris <mharris@redhat.com> 2.0-2
- Replaced the temporary tongue-in-cheek humourous package summary and
  description with the proper package descriptions, as many people didn't get
  the joke, while others felt it was getting old.  Ah well, I had my fun for
  a while anyway.  ;o)

* Wed Nov 30 2005 Mike A. Harris <mharris@redhat.com> 2.0-1
- Updated libdrm to version 2.0 from dri.sf.net.  This is an ABI incompatible
  release, meaning everything linked to it needs to be recompiled.

* Tue Nov 01 2005 Mike A. Harris <mharris@redhat.com> 1.0.5-1
- Updated libdrm to version 1.0.5 from dri.sf.net upstream to work around
  mesa unichrome dri driver compile failure.

* Mon Oct 24 2005 Mike A. Harris <mharris@redhat.com> 1.0.4-1
- Updated libdrm to version 1.0.4 from X11R7 RC1
- Remove i915_drv.h, imagine_drv.h, mach64_drv.h, mga_drv.h, mga_ucode.h,
  r128_drv.h, radeon_drv.h, savage_drv.h, sis_drv.h, sis_ds.h, tdfx_drv.h,
  via_drv.h, via_ds.h, via_mm.h, via_verifier.h from file manifest.

* Tue Oct 04 2005 Mike A. Harris <mharris@redhat.com> 1.0.3-3
- Update BuildRoot to use Fedora Packaging Guidelines.
- Add missing "BuildRequires: libX11-devel, pkgconfig"

* Thu Sep 29 2005 Mike A. Harris <mharris@redhat.com> 1.0.3-2
- Add missing documentation to doc macro
- Fix spec file project URL

* Sat Sep 03 2005 Mike A. Harris <mharris@redhat.com> 1.0.3-1
- Initial build.
