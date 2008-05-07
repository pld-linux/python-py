#
# TODO:
# - cleanup ;)
# - some arch-depended libraries in sitescript_dir
# - documentation and examples in sitescript_dir
%define		module	py
#
Summary:	Agile development and test support library
Summary(pl.UTF-8):	Zwinna biblioteka obsługująca rozwój i testowanie
Name:		python-%{module}
Version:	0.9.0
Release:	0.1
License:	MIT license
Group:		Development/Languages/Python
Source0:	http://codespeak.net/download/py/%{module}-%{version}.tar.gz
# Source0-md5:	adecd7befdfa431341c8e09e0bc94ca3
URL:		http://codespeak.net/py/
BuildRequires:	FHS-fix(arch-dependent files in /usr/share)
BuildRequires:	python-devel >= 1:2.5
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The py lib is a development support library featuring py.test, ad-hoc
distributed execution, micro-threads and svn abstractions.

%description -l pl.UTF-8
Biblioteka py wspiera rozwijanie oprogramowania udostępniając py.test,
rozproszone wykonywanie kodu, mikrowątki i abstrakcję svn.

%prep
%setup -q -n %{module}-%{version}

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT

%{__python} setup.py install \
	--root=$RPM_BUILD_ROOT \
	--optimize=2

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{py_sitescriptdir}/py
%{py_sitescriptdir}/py-*.egg-info
