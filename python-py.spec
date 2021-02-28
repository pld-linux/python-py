#
# Conditional build:
%bcond_without	doc	# HTML documentation build
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module
%bcond_with	tests	# unit tests [fail with pytest 3.0?]

%define		module	py
Summary:	Library with cross-python path, ini-parsing, io, code, log facilities
Summary(pl.UTF-8):	Biblioteka wspierająca obsługę ścieżek, ini, we/wy, kodowania i logowania w wielu Pythonach
Name:		python-%{module}
Version:	1.10.0
Release:	3
License:	MIT
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/py/
Source0:	https://files.pythonhosted.org/packages/source/p/py/py-%{version}.tar.gz
# Source0-md5:	5f108bfe00d5468cbdb8071051f86a55
URL:		https://pypi.org/project/py/
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools >= 7.0
BuildRequires:	python-setuptools_scm
%if %{with tests}
%if %(locale -a | grep -q '^C\.utf8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
BuildRequires:	python-pytest >= 2.9.0
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.4
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools >= 7.0
BuildRequires:	python3-setuptools_scm
%if %{with tests}
%if %(locale -a | grep -q '^C\.utf8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
BuildRequires:	python3-pytest >= 2.9.0
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
%{?with_doc:BuildRequires:	sphinx-pdg >= 1.0}
%{?with_doc:BuildRequires:	python-devel-tools}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The py lib is a Python development support library featuring the
following tools and modules:
 - py.path: uniform local and svn path objects
 - py.apipkg: explicit API control and lazy-importing
 - py.iniconfig: easy parsing of .ini files
 - py.code: dynamic code generation and introspection

%description -l pl.UTF-8
Biblioteka py to biblioteka wpierająca tworzenie oprogramowania w
Pythonie. Zawiera następujące narzędzia i moduły:
 - py.path - jednolite obiekty ścieżek lokalnych i svn
 - py.apipkg - bezpośrednia kontrola API i leniwego importowania
 - py.iniconfig - łatwa analiza plików .ini
 - py.code - dynamiczne generowanie kodu i introspekcji

%package -n python3-py
Summary:	Library with cross-python path, ini-parsing, io, code, log facilities
Summary(pl.UTF-8):	Biblioteka wspierająca obsługę ścieżek, ini, we/wy, kodowania i logowania w wielu Pythonach
Group:		Development/Languages/Python

%description -n python3-py
The py lib is a Python development support library featuring the
following tools and modules:
- py.path: uniform local and svn path objects
- py.apipkg: explicit API control and lazy-importing
- py.iniconfig: easy parsing of .ini files
- py.code: dynamic code generation and introspection

%description -n python3-py -l pl.UTF-8
Biblioteka py to biblioteka wpierająca tworzenie oprogramowania w
Pythonie. Zawiera następujące narzędzia i moduły:
 - py.path - jednolite obiekty ścieżek lokalnych i svn
 - py.apipkg - bezpośrednia kontrola API i leniwego importowania
 - py.iniconfig - łatwa analiza plików .ini
 - py.code - dynamiczne generowanie kodu i introspekcji

%package apidocs
Summary:	Documentation for Python py library
Summary(pl.UTF-8):	Dokumentacja do biblioteki Pythona py
Group:		Documentation

%description apidocs
Documentation for Python py library.

%description apidocs -l pl.UTF-8
Dokumentacja do biblioteki Pythona py.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
LC_ALL=C.UTF-8 \
%{__python} -m pytest testing
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
LC_ALL=C.UTF-8 \
%{__python3} -m pytest testing
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C doc html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG.rst LICENSE README.rst
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-py
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG.rst LICENSE README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/{_modules,_static,announce,*.html,*.js}
%endif
