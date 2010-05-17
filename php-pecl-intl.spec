%define		modname		intl
%define		status		stable
Summary:	%{modname} - Internationalization extension
Summary(pl.UTF-8):	%{modname} - rozszerzenie internacjonalizacji
Name:		php-pecl-%{modname}
Version:	1.1.0
Release:	1
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	650f59a78650f4557f3bf8745ce2c663
Patch0:		%{name}-tsrm.patch
URL:		http://pecl.php.net/package/intl/
BuildRequires:	libicu-devel >= 3.4.0-1
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
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
%patch0 -p2

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
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
%doc doc CREDITS
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
