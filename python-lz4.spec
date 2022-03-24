#
# TODO: versions 3.0.0+ support only python 3.6+
#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module	lz4
Summary:	LZ4 bindings for Python
Summary(pl.UTF-8):	Wiązania LZ4 dla Pythona
Name:		python-%{module}
# keep 2.x here for python2 support
Version:	2.2.1
Release:	2
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/lz4/
Source0:	https://files.pythonhosted.org/packages/source/l/lz4/lz4-%{version}.tar.gz
# Source0-md5:	778661bc5271b5befe11ee127c252a5d
URL:		https://github.com/python-lz4/python-lz4
BuildRequires:	lz4-devel >= 1:1.7.5
BuildRequires:	py3c >= 1.0
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-pkgconfig
BuildRequires:	python-setuptools
BuildRequires:	python-setuptools_scm
%if %{with tests}
BuildRequires:	python-future
BuildRequires:	python-psutil
BuildRequires:	python-pytest >= 3.3.1
BuildRequires:	python-pytest-cov
BuildRequires:	python-pytest-runner
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.4
BuildRequires:	python3-pkgconfig
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_scm
%if %{with tests}
BuildRequires:	python3-psutil
BuildRequires:	python3-pytest >= 3.3.1
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-pytest-runner
%endif
%endif
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python-sphinx_bootstrap_theme
BuildRequires:	sphinx-pdg-2 >= 1.6.0
%endif
Requires:	lz4-libs >= 1:1.7.5
Requires:	python-modules >= 1:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides python bindings for the LZ4 compression library.

%package -n python3-%{module}
Summary:	LZ4 bindings for Python
Summary(pl.UTF-8):	Wiązania LZ4 dla Pythona
Group:		Libraries/Python
Requires:	lz4-libs >= 1:1.7.5
Requires:	python3-modules >= 1:3.4

%description -n python3-%{module}
This package provides python bindings for the LZ4 compression library.

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Python %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/$(echo build-2/lib.*):$(pwd) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-2
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
%doc LICENSE README.rst
%dir %{py_sitedir}/%{module}
%{py_sitedir}/%{module}/*.py[co]
%dir %{py_sitedir}/%{module}/block
%{py_sitedir}/%{module}/block/*.py[co]
%dir %{py_sitedir}/%{module}/frame
%{py_sitedir}/%{module}/frame/*.py[co]
%attr(755,root,root) %{py_sitedir}/%{module}/*.so
%attr(755,root,root) %{py_sitedir}/%{module}/block/*.so
%attr(755,root,root) %{py_sitedir}/%{module}/frame/*.so
%{py_sitedir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc LICENSE README.rst
%dir %{py3_sitedir}/%{module}
%{py3_sitedir}/%{module}/*.py
%dir %{py3_sitedir}/%{module}/block
%{py3_sitedir}/%{module}/block/*.py
%dir %{py3_sitedir}/%{module}/frame
%{py3_sitedir}/%{module}/frame/*.py
%attr(755,root,root) %{py3_sitedir}/%{module}/*.so
%attr(755,root,root) %{py3_sitedir}/%{module}/block/*.so
%attr(755,root,root) %{py3_sitedir}/%{module}/frame/*.so
%{py3_sitedir}/%{module}/__pycache__
%{py3_sitedir}/%{module}/block/__pycache__
%{py3_sitedir}/%{module}/frame/__pycache__
%{py3_sitedir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
