#
# Conditional build:
%bcond_without	doc	# HTML documentation build
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module	py
Summary:	Library with cross-python path, ini-parsing, io, code, log facilities
Summary(pl.UTF-8):	Biblioteka wspierająca obsługę ścieżek, ini, we/wy, kodowania i logowania w wielu Pythonach
Name:		python-%{module}
Version:	1.4.31
Release:	1
License:	MIT
Group:		Development/Languages/Python
Source0:	https://pypi.python.org/packages/source/p/py/py-%{version}.tar.gz
# Source0-md5:	5d2c63c56dc3f2115ec35c066ecd582b
Source1:	http://docs.python.org/objects.inv?/python-objects.inv
# Source1-md5:	3d3c0b594b2e91d559418c107d973633
Patch0:		%{name}-offline.patch
URL:		https://pypi.python.org/pypi/py
%if %{with python2}
BuildRequires:	python-devel >= 1:2.5
BuildRequires:	python-setuptools >= 7.0
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools >= 7.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
%{?with_doc:BuildRequires:	sphinx-pdg >= 1.0}
%{?with_doc:BuildRequires:	python-devel-tools}
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

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1

cp -p %{SOURCE1} doc

%build
%if %{with python2}
%py_build \
	--build-base build-2
%endif

%if %{with python3}
%py3_build \
	--build-base build-3
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
%{__python3} -- setup.py \
	build --build-base build-3 \
	install \
	--root=$RPM_BUILD_ROOT \
	--optimize=2

%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/py/test.py
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGELOG LICENSE README.txt %{?with_doc:doc/_build/html}
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-py
%defattr(644,root,root,755)
%doc CHANGELOG LICENSE README.txt %{?with_doc:doc/_build/html}
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif
