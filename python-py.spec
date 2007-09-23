#
# TODO:
# - cleanup ;)
# - some arch-depended libraries in sitescript_dir
# - documentation and examples in sitescript_dir
%define		module	py
#
Summary:	agile development and test support library
Summary(pl.UTF-8):	zwinna biblioteka obsługująca rozwój i testowanie
Name:		python-%{module}
Version:	0.9.0
Release:	0.1
License:	MIT license
Group:		Development/Languages/Python
Source0:	http://codespeak.net/download/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	adecd7befdfa431341c8e09e0bc94ca3
URL:		http://codespeak.net/py/
BuildRequires:	python-devel
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
the py lib is a development support library featuring py.test, ad-hoc
distributed execution, micro-threads and svn abstractions.

%prep
%setup -q -n %{module}-%{version}

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT

python setup.py install \
	--root=$RPM_BUILD_ROOT \
	--optimize=2

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{py_sitescriptdir}/py
