#
# Conditional build:
%bcond_without	doc	# HTML documentation build
#
%define		module	py
#
Summary:	Library with cross-python path, ini-parsing, io, code, log facilities
Summary(pl.UTF-8):	Biblioteka wspierająca obsługę ścieżek, ini, we/wy, kodowania i logowania w wielu Pythonach
Name:		python-%{module}
Version:	1.4.9
Release:	1
License:	MIT
Group:		Development/Languages/Python
Source0:	http://pypi.python.org/packages/source/p/py/%{module}-%{version}.zip
# Source0-md5:	471a88edcdae2f9689c0193972a1a1f8
Source1:	http://docs.python.org/objects.inv#/python-objects.inv
# Source1-md5:	9128e774ec21dcd62dc5bca61cdd91ee
Patch0:		%{name}-offline.patch
URL:		http://pylib.org/
BuildRequires:	python-devel >= 1:2.5
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%{?with_doc:BuildRequires:	sphinx-pdg >= 1.0}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The py lib is a Python development support library featuring the
following tools and modules:
 - py.path:  uniform local and svn path objects
 - py.apipkg:  explicit API control and lazy-importing
 - py.iniconfig:  easy parsing of .ini files
 - py.code: dynamic code generation and introspection

%description -l pl.UTF-8
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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG LICENSE README.txt %{?with_doc:doc/_build/html}
%{py_sitescriptdir}/py
%{py_sitescriptdir}/py-%{version}-py*.egg-info
