Name:           tiger
Version:        3.2.3
Release:        13%{?dist}
Epoch:          1
Summary:        Security auditing on UNIX systems

Group:          Applications/System
License:        GPL+
URL:            http://www.nongnu.org/tiger/
Source0:        http://git.savannah.gnu.org/cgit/tiger.git/snapshot/tiger-version_3_2_3.tar.gz
#Source1:        http://savannah.nongnu.org/download/tiger/tiger-3.2.1.tar.gz.sig
Source2:        tiger.cron
Source3:        tiger.ignore
Source4:        tiger.ignore.server
Source5:        tiger.README
Source6:        tiger.logrotate
Patch0:         tiger-3.2.1-autotools.patch
# Default configuration
Patch1:         tiger-3.2.1-config.patch
# Mainly typos
Patch2:         tiger-3.2.1-doc.patch
# Fixes in the checking scripts and additional scripts
Patch3:         tiger-3.2.1-scripts.patch
# Various fixes
Patch4:         tiger-3.2.1-fixes.patch
# Fix for one small C program
Patch5:         tiger-3.2.1-gcc4.patch
# add more local file system
Patch6:         tiger-3.2.1-localfs.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  autoconf, recode
Requires:       bash, vixie-cron

%description
TIGER, or the "tiger" scripts, is a set of Bourne shell scripts,
C programs and data files which are used to perform a security audit
of UNIX systems.  It is designed to hopefully be easy to use, easy to
understand and easy to enhance.


%prep
%setup -q -n tiger
%patch0 -p1 -b .autotools
%patch1 -p1 -b .config
# No backup, or the files will be copied in the buildroot
#%patch2 -p1 -b .doc 
#%patch3 -p1 -b .scripts
%patch2 -p1
%patch3 -p1
%patch4 -p1 -b .fixes
%patch5 -p1 -b .gcc4
%patch6 -p1 -b .localfs
find . -name "*.rpmorig" | xargs rm -f
find . -name "*.orig" | xargs rm -f
find . -name "*.old" | xargs rm -f
recode ISO-8859-1..UTF-8 man/tiger.8.in
recode ISO-8859-1..UTF-8 README.hostids
recode ISO-8859-1..UTF-8 README.linux
install -p -m 644 %{SOURCE5} README.Fedora
recode ISO-8859-1..UTF-8 README.Fedora
recode ISO-8859-1..UTF-8 README.ignore
# Remove CVS dirs
find . -type d -name CVS | xargs rm -rf


%build
autoconf
%configure  \
    --with-tigerhome=%{_libdir}/tiger \
    --with-tigerwork=%{_localstatedir}/run/tiger/work \
    --with-tigerlog=%{_localstatedir}/log/tiger \
    --with-tigerbin=%{_sbindir} \
    --with-tigerconfig=%{_sysconfdir}/tiger

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/cron.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/tiger/templates
install -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/tiger
install -p -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/tiger/tiger.ignore
install -p -m 644 version.h $RPM_BUILD_ROOT%{_libdir}/tiger
for system in AIX HPUX IRIX NeXT SunOS UNICOS UNICOSMK Tru64 MacOSX; do
  rm -rf $RPM_BUILD_ROOT%{_libdir}/tiger/systems/${system};
done

ln -s %{_sbindir}/tigexp $RPM_BUILD_ROOT%{_libdir}/tiger/tigexp

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -p -m 644 %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/tiger

mkdir examples
cp -p cronrc tigerrc tigerrc-all tigerrc-dist tigerrc-TAMU \
      site-sample site-saturn %{SOURCE4} %{SOURCE6} examples
chmod 644 examples/*

# Perm fixes
chmod +x $RPM_BUILD_ROOT%{_libdir}/tiger/systems/Linux/2/check_*
chmod 644  $RPM_BUILD_ROOT%{_sysconfdir}/tiger/tigerrc
chmod 755 $RPM_BUILD_ROOT%{_localstatedir}/run/tiger/work
chmod 644  $RPM_BUILD_ROOT%{_sysconfdir}/tiger/cronrc

# Documentation (in %%doc)
rm -rf $RPM_BUILD_ROOT%{_libdir}/tiger/html


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc USING BUGS.EXTERN DESCRIPTION CREDITS README README.1st README.hostids 
%doc README.ignore README.linux README.signatures README.sources
%doc README.time README.unsupported README.writemodules TODO README.Fedora
%doc COPYING examples html
%{_mandir}/man*/*
%{_sbindir}/*
%{_libdir}/tiger
%{_localstatedir}/run/tiger
%defattr(-,root,root,755)
%dir %{_localstatedir}/log/tiger
%config(noreplace) %{_sysconfdir}/tiger
%config(noreplace) %{_sysconfdir}/cron.d/tiger
%config(noreplace) %{_sysconfdir}/logrotate.d/tiger



%changelog
* Tue Sep 06 2011 DeoGracia <deogracia@free.fr> - 1:3.2.1-13
- Forget to add tiger-3.2.1-localfs.patch in spec file in last release

* Tue Sep 06 2011 DeoGracia <deogracia@free.fr> - 1:3.2.1-12
- Add ext3 and ext4 to local filesystem

* Sun Sep 04 2011 DeoGracia <deogracia@free.fr> - 1:3.2.1-11
- Build for Centos

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar 08 2009 Caolán McNamara <caolanm@redhat.com> 3.2.1-10
- defuzz patches to rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.2.1-8
- Autorebuild for GCC 4.3

* Fri Sep 08 2006 Aurelien Bompard <abompard@fedoraproject.org> 3.2.1-6
- rebuild

* Thu Aug 31 2006 Aurelien Bompard <abompard@fedoraproject.org> 3.2.1-5
- rebuild

* Sat May 13 2006 Aurelien Bompard <gauret[AT]free.fr> 3.2.1-4
- include the COPYING file
- put HTML doc in %%doc
- drop useless logos
- fix %%description
- remove CVS dirs in %%prep
- Thanks to Hans de Goede in bug 165311

* Sat Apr 22 2006 Aurelien Bompard <gauret[AT]free.fr> 3.2.1-3
- don't backup some patches, or the files will be copied in the buildroot
- set conf files to noreplace
- fix manpage encoding

* Sun Apr 02 2006 Aurelien Bompard <gauret[AT]free.fr> 3.2.1-2
- fix arguments for "sort" and "tail" in patch3

* Sat Aug 06 2005 Aurelien Bompard <gauret[AT]free.fr> 3.2.1-1
- initial package, importing Debian's fixes
