%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%global php_extdir  %(php-config --extension-dir 2>/dev/null || echo "undefined")
%global php_version %(php-config --version 2>/dev/null || echo 0)

Name:           php-xcache
Version:        3.0.0
Release:        1%{?dist}
Summary:        XCache is a fast, stable  PHP opcode cacher

Group:          Development/Languages
License:        BSD
URL:            http://xcache.lighttpd.net
Source0:        http://xcache.lighttpd.net/pub/Releases/3.0.0/xcache-3.0.0.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  php-devel
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}

%description
XCache is a fast, stable  PHP opcode cacher that has been tested and is now
running on production servers under high load. It is tested (on Linux) and 
supported on all of the latest  PHP release branches such as PHP_5_1 PHP_5_2 
PHP_5_3 PHP_5_4. ThreadSafe/Windows is also perfectly supported. It overcomes 
a lot of problems that has been with other competing opcachers such as being 
able to be used with new  PHP versions.


%prep
%setup -q -n xcache-%{version}


%build
phpize
%configure \
  --with-libdir=%{_lib} \
  --enable-xcache \
  --enable-xcache-constant \
  --enable-xcache-optimizer \
  --enable-xcache-coverager \
  --enable-xcache-assembler \
  --enable-xcache-encoder  \
  --enable-xcache-decoder

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
#make install DESTDIR=$RPM_BUILD_ROOT
make install INSTALL_ROOT=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/php.d
cp -p xcache.ini $RPM_BUILD_ROOT%{_sysconfdir}/php.d

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README THANKS
%config(noreplace) /%{php_inidir}/xcache.ini
%{php_extdir}/xcache.so


%changelog
* Wed Nov 21 2012 Deogracia <deogracia@free.fr> 3.0.0-1
- first build
