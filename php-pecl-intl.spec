%define		php_name	php%{?php_suffix}
%define		modname		intl
%define		status		stable
Summary:	%{modname} - Internationalization extension
Summary(pl.UTF-8):	%{modname} - rozszerzenie internacjonalizacji
Name:		%{php_name}-pecl-%{modname}
Version:	1.1.2
Release:	1
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	6e32eb19a8920c48f88571eb2e9d2213
Patch0:		zend_arg_info_static.patch
Patch1:		z_refcount.patch
URL:		http://pecl.php.net/package/intl/
BuildRequires:	%{php_name}-devel >= 3:5.0.0
BuildRequires:	libicu-devel >= 3.4.0-1
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	re2c
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Provides:	php(intl)
Obsoletes:	php-pecl-idn
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Internationalization extension implements ICU library functionality in
PHP.

Since 1.0.2 it also integrates IDN functions.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
Rozszerzenie to posiada zaimplementowaną obsługę biblioteki ICU.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}/* .
%if "%{php_major_version}.%{php_minor_version}" >= "5.3"
%patch0 -p1
%patch1 -p1
%endif

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	EXTENSION_DIR=%{php_extensiondir} \
	INSTALL_ROOT=$RPM_BUILD_ROOT
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc doc/* CREDITS
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
