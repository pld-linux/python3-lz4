# Conditional build:
%bcond_with	doc	# don't build doc
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	lz4
Summary:	LZ4 bindings for Python
Name:		python-%{module}
Version:	2.1.6
Release:	2
License:	BSD
Group:		Libraries/Python
Source0:	http://pypi.debian.net/lz4/lz4-%{version}.tar.gz
# Source0-md5:	badde942dabaac89256243b87977c49c
URL:		https://github.com/python-lz4/python-lz4
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-devel
%if %{with tests}
BuildRequires:	python-future
BuildRequires:	python-pytest-cov
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel
%if %{with tests}
BuildRequires:	python3-future
BuildRequires:	python3-pytest-cov
%endif
%endif
BuildRequires:	lz4-devel >= 1.7.5
Requires:	python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides python bindings for the LZ4 compression library.

%package -n python3-%{module}
Summary:	LZ4 bindings for Python
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}
This package provides python bindings for the LZ4 compression library.

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

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
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
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
%doc README.rst
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
%doc README.rst
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
%doc docs/_build/html/*
%endif
