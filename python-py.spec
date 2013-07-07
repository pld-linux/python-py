#
# Conditional build:
%bcond_without	doc	# HTML documentation build
%bcond_without	python3 # CPython 3.x module

%define		module	py
Summary:	Library with cross-python path, ini-parsing, io, code, log facilities
Summary(pl.UTF-8):	Biblioteka wspierająca obsługę ścieżek, ini, we/wy, kodowania i logowania w wielu Pythonach
Name:		python-%{module}
Version:	1.4.13
Release:	2
License:	MIT
Group:		Development/Languages/Python
Source0:	http://pypi.python.org/packages/source/p/py/py-%{version}.tar.gz
# Source0-md5:	3857dc8309d5f284669b81184253c2bb
Source1:	http://docs.python.org/objects.inv?/python-objects.inv
# Source1-md5:	3d3c0b594b2e91d559418c107d973633
Patch0:		%{name}-offline.patch
URL:		http://pylib.org/
BuildRequires:	python-devel >= 1:2.5
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%{?with_doc:BuildRequires:	sphinx-pdg >= 1.0}
%{?with_doc:BuildRequires:	python-devel-tools}
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-modules
BuildRequires:	python3-distribute
%endif
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
%{__python} setup.py build

%if %{with python3}
%{__python3} setup.py \
	build -b build-3
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C doc html
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--root=$RPM_BUILD_ROOT \
	--optimize=2

%py_postclean

%if %{with python3}
%{__python3} -- setup.py \
	build -b build-3 \
	install \
	--root=$RPM_BUILD_ROOT \
	--optimize=2

%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/py/test.py
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG LICENSE README.txt %{?with_doc:doc/_build/html}
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info

%if %{with python3}
%files -n python3-py
%defattr(644,root,root,755)
%doc CHANGELOG LICENSE README.txt %{?with_doc:doc/_build/html}
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif
