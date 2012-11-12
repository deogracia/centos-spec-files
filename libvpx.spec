Name:			libvpx
Summary:		VP8 Video Codec SDK
Version:		v1.1.0
Release:		1%{?dist}
License:		BSD
Group:			System Environment/Libraries
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:		http://webm.googlecode.com/files/%{name}-%{version}.tar.bz2
# Thanks to debian.
Source2:		libvpx.ver
URL:			http://www.webmproject.org/tools/vp8-sdk/
BuildRequires:		doxygen, php-cli

%description
libvpx provides the VP8 SDK, which allows you to integrate your applications 
with the VP8 video codec, a high quality, royalty free, open source codec 
deployed on millions of computers and devices worldwide. 

%package devel
Summary:		Development files for libvpx
Group:			Development/Libraries
Requires:		%{name} = %{version}-%{release}

%description devel
Development libraries and headers for developing software against 
libvpx.

%prep
%setup -q

%build
%ifarch %{ix86}
%global vpxtarget x86-linux-gcc
%else
%ifarch	x86_64
%global	vpxtarget x86_64-linux-gcc
%else
%global vpxtarget generic-gnu
%endif
%endif

./configure \
  --prefix=%{_prefix} \
  --libdir=%{_libdir} \
  --target=%{vpxtarget} \
  --enable-pic \
  --disable-install-srcs \
  --enable-vp8 \
  --enable-postproc \
  --enable-onthefly-bitpacking \
  --enable-runtime-cpu-detect \
  --enable-shared \
  --enable-multi-res-encoding \
  --enable-postproc-visualizer \
  --enable-error-concealment \
  --disable-examples \
  --enable-install-docs \
  --enable-small

# Hack our optflags in.
sed -i "s|\"vpx_config.h\"|\"vpx_config.h\" %{optflags} -fPIC|g" libs-%{vpxtarget}.mk
#sed -i "s|\"vpx_config.h\"|\"vpx_config.h\" %{optflags} -fPIC|g" examples-%{vpxtarget}.mk
sed -i "s|\"vpx_config.h\"|\"vpx_config.h\" %{optflags} -fPIC|g" docs-%{vpxtarget}.mk
make %{?_smp_mflags} verbose=true target=libs

# Really? You couldn't make this a shared library? Ugh.
# Oh well, I'll do it for you.
mkdir tmp
cd tmp
ar x ../libvpx_g.a
cd ..
gcc -fPIC -shared -pthread -lm -Wl,--no-undefined -Wl,-soname,libvpx.so.0 -Wl,--version-script,%{SOURCE2} -Wl,-z,noexecstack -o libvpx.so.0.0.0 tmp/*.o 
rm -rf tmp

# Temporarily dance the static libs out of the way
mv libvpx.a libNOTvpx.a
mv libvpx_g.a libNOTvpx_g.a

# We need to do this so the examples can link against it.
ln -sf libvpx.so.0.0.0 libvpx.so

#make %{?_smp_mflags} verbose=true target=examples
make %{?_smp_mflags} verbose=true target=docs

# Put them back so the install doesn't fail
mv libNOTvpx.a libvpx.a
mv libNOTvpx_g.a libvpx_g.a

%install
rm -rf $RPM_BUILD_ROOT
make DIST_DIR=%{buildroot}%{_prefix} install

mkdir -p %{buildroot}%{_includedir}/vpx/
install -p libvpx.so.0.0.0 %{buildroot}%{_libdir}
pushd %{buildroot}%{_libdir}
ln -sf libvpx.so.0.0.0 libvpx.so
ln -sf libvpx.so.0.0.0 libvpx.so.0
ln -sf libvpx.so.0.0.0 libvpx.so.0.0
popd
pushd %{buildroot}
# Stuff we don't need.
rm -rf usr/build/ usr/md5sums.txt usr/lib*/*.a usr/CHANGELOG usr/README
popd

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS CHANGELOG LICENSE README
%{_libdir}/libvpx.so.*

%files devel
%defattr(-,root,root,-)
# These are SDK docs, not really useful to an end-user.
%doc docs/
%{_includedir}/vpx/
%{_libdir}/pkgconfig/vpx.pc
%{_libdir}/libvpx.so

%changelog
* Mon Nov 12 2012 Deogracia <deogracia@free.fr> v1.1.0-1.el6
- update to upstream v1.1.0
- remove all patch : seems not needed anymore
- remove embeded libvpv.pc : use the one from upstream

* Mon Dec 06 2010 Benjamin Otte <otte@redhat.com> 0.9.0-8
- Fix CVE-2010-4203
Resolves: rhbz#652440

* Wed Jun 27 2010 Benjamin Otte <otte@redhat.com> 0.9.0-7
- Import 0.9.0-6 package from Fedora
- Add patch porting yasm syntax to gas
Related: rhbz#603113
