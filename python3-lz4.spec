#
# Conditional build:
%bcond_without	doc		# Sphinx documentation
%bcond_without	experimental	# experimenal lz4.stream API
%bcond_without	tests		# unit tests

%define		module	lz4
Summary:	LZ4 bindings for Python
Summary(pl.UTF-8):	Wiązania LZ4 dla Pythona
Name:		python3-%{module}
Version:	4.3.2
Release:	3
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/lz4/
Source0:	https://files.pythonhosted.org/packages/source/l/lz4/lz4-%{version}.tar.gz
# Source0-md5:	12bf7614d70e36f8c3317cd11b5955ad
URL:		https://github.com/python-lz4/python-lz4
BuildRequires:	lz4-devel >= 1:1.7.5
BuildRequires:	python3-devel >= 1:3.7
BuildRequires:	python3-pkgconfig
BuildRequires:	python3-setuptools >= 1:45
BuildRequires:	python3-setuptools_scm >= 6.2
BuildRequires:	python3-toml
%if %{with tests}
BuildRequires:	python3-psutil
BuildRequires:	python3-pytest >= 3.3.1
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-pytest-runner
%endif
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinx_bootstrap_theme
BuildRequires:	sphinx-pdg-3 >= 1.6.0
%endif
Requires:	lz4-libs >= 1:1.7.5
Requires:	python3-modules >= 1:3.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
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
%{?with_experimental:export PYLZ4_EXPERIMENTAL=1}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests/block tests/frame %{?with_experimental:tests/stream} -k 'not test_block_decompress_mem_usage'
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/$(echo build-3/lib.*):$(pwd) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{?with_experimental:export PYLZ4_EXPERIMENTAL=1}

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%dir %{py3_sitedir}/%{module}
%attr(755,root,root) %{py3_sitedir}/%{module}/*.so
%{py3_sitedir}/%{module}/*.py
%{py3_sitedir}/%{module}/__pycache__
%dir %{py3_sitedir}/%{module}/block
%attr(755,root,root) %{py3_sitedir}/%{module}/block/*.so
%{py3_sitedir}/%{module}/block/*.py
%{py3_sitedir}/%{module}/block/__pycache__
%attr(755,root,root) %{py3_sitedir}/%{module}/frame/*.so
%dir %{py3_sitedir}/%{module}/frame
%{py3_sitedir}/%{module}/frame/*.py
%{py3_sitedir}/%{module}/frame/__pycache__
%if %{with experimental}
%attr(755,root,root) %{py3_sitedir}/%{module}/stream/*.so
%dir %{py3_sitedir}/%{module}/stream
%{py3_sitedir}/%{module}/stream/*.py
%{py3_sitedir}/%{module}/stream/__pycache__
%endif
%{py3_sitedir}/%{module}-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
