Summary: Audio Video	 Standard of China
Name: xavs
Version: 0.1.51
Release: 3%{?dist}
License: GPL
Group: System Environment/Libraries
URL: http://xavs.sourceforge.net/
Source0: %{name}-trunk.tar.gz

%description
AVS is the Audio Video Standard of China.  This project aims to
implement high quality AVS encoder and decoder.

%package devel
Group: Development/Libraries
Summary: Development interfaces for xavs
Requires: xavs >= %{version}

%description devel
devel files for xavs

%prep
%setup -q -n trunk

%build
export CFLAGS="%{optflags}"
./configure \
  --bindir=%{_bindir} \
  --libdir=%{_libdir} \
  --includedir=%{_includedir} \
  --enable-pic --enable-shared

%install
rm -rf %{buildroot}
make install \
  DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc doc/*.txt
%{_bindir}/xavs

%files devel
%defattr(-,root,root,-)
%{_includedir}/xavs.h
%{_libdir}/libxavs.a
%{_libdir}/libxavs.so
%{_libdir}/libxavs.so.1
%{_libdir}/pkgconfig/xavs.pc
#   /usr/include/xavs.h
#   /usr/lib64/libxavs.a
#   /usr/lib64/libxavs.so
#   /usr/lib64/libxavs.so.1
#   /usr/lib64/pkgconfig/xavs.pc

%changelog
* Sat Nov 03 2012 Deogracia <deogracia@free.fr> - 0.1.51-3
- Rebuild for Centos
- Add devel package

* Mon Mar 14 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.1.51-2
- Initial build.

