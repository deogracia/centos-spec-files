Name:		ffmpeg2theora
Version:	0.27
Release:	2%{?dist}

Summary:	Convert any file that ffmpeg can decode to theora
Group:		Applications/Multimedia
License:	GPLv2+
URL:		http://v2v.cc/~j/ffmpeg2theora/
Source0:	http://v2v.cc/~j/ffmpeg2theora/downloads/ffmpeg2theora-%{version}.tar.bz2
Patch0:		ffmpeg2theora-0.27-ldflags.patch
BuildRequires:	scons, ffmpeg-devel, libkate-devel, libogg-devel >= 1.1
BuildRequires:	libtheora-devel >= 1.1.0, libvorbis-devel


%description
With ffmpeg2theora you can convert any file that ffmpeg can
decode to theora. right now the settings are hardcoded into
the binary. the idea is to provide ffmpeg2theora as a binary
along sites like v2v.cc to enable as many people as possible
to encode video clips with the same settings.


%prep
%setup -q
%patch0 -p1 -b .ldflags


%build
scons APPEND_CCFLAGS="$RPM_OPT_FLAGS"


%install
rm -rf %{buildroot}
scons install destdir="%{buildroot}" prefix=%{_prefix}
mkdir -p %{buildroot}%{_mandir}/man1
mv %{buildroot}%{_prefix}/man/man1/ffmpeg2theora.1 %{buildroot}%{_mandir}/man1
rm -rf %{buildroot}%{_prefix}/man


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,0755)
%doc ChangeLog README TODO AUTHORS COPYING
%{_bindir}/ffmpeg2theora
%{_mandir}/man1/ffmpeg2theora.1.gz


%changelog
* Sun May 13 2012 LTN Packager <packager-el6rpms@LinuxTECH.NET> - 0.27-2
- rebuilt for updated ffmpeg-libs

* Tue Jul 05 2011 LTN Packager <packager-el6rpms@LinuxTECH.NET> - 0.27-1
- spec-file imported from Fedora
- cleaned up spec-file

