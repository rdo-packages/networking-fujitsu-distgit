# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif

%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global plugin_name networking-fujitsu
%global src_name networking_fujitsu

%global common_desc \
This package contains Fujitsu neutron plugins

Name:           python-%{plugin_name}
Version:        XXX
Release:        XXX
Summary:        FUJITSU ML2 plugins/drivers for OpenStack Neutron
License:        ASL 2.0
URL:            https://pypi.python.org/pypi/%{plugin_name}
Source0:        https://tarballs.openstack.org/%{plugin_name}/%{plugin_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

BuildRequires:  git
BuildRequires:  python%{pyver}-hacking
BuildRequires:  python%{pyver}-subunit
BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-oslo-sphinx
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  /usr/bin/stestr-%{pyver}
BuildRequires:  python%{pyver}-testscenarios
BuildRequires:  python%{pyver}-testtools
BuildRequires:  python%{pyver}-reno
BuildRequires:  python%{pyver}-testresources
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-oslo-i18n
BuildRequires:  python%{pyver}-oslo-utils
BuildRequires:  openstack-neutron
BuildRequires:  python%{pyver}-neutron-tests
BuildRequires:  python%{pyver}-neutron-lib-tests
BuildRequires:  python%{pyver}-mock
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python%{pyver}-%{plugin_name}
Summary:  neutron ML2 plugin for Fujitsu switch
%{?python_provide:%python_provide python%{pyver}-%{plugin_name}}

Requires:       python%{pyver}-oslo-i18n >= 3.15.3
Requires:       python%{pyver}-oslo-utils >= 3.33.0
Requires:       python%{pyver}-oslo-log >= 3.36.0
Requires:       python%{pyver}-pbr >= 2.0.0
Requires:       python%{pyver}-six
Requires:       openstack-neutron-common >= 1:13.0.0
Requires:       openstack-neutron-ml2 >= 1:13.0.0
Requires:       python%{pyver}-oslo-config
Requires:       python%{pyver}-eventlet
Requires:       python%{pyver}-neutron-lib >= 1.18.0
Requires:       python%{pyver}-paramiko >= 2.0.0

%description -n python%{pyver}-%{plugin_name}
%{common_desc}

%prep
%autosetup -n %{plugin_name}-%{upstream_version} -S git
%py_req_cleanup

%build
%{pyver_build}

# oslosphinx do not work with sphinx > 2
%if %{pyver} == 2
sphinx-build-%{pyver} -W -b html doc/source html
rm -rf html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}
install -d -m 755 %{buildroot}%{_sysconfdir}/neutron/plugins/ml2/
mv %{buildroot}/usr/etc/neutron/plugins/ml2/*.ini %{buildroot}%{_sysconfdir}/neutron/plugins/ml2/

%check
export PYTHON=%{pyver_bin}
stestr-%{pyver} run

%files -n python%{pyver}-%{plugin_name}
%license LICENSE
%doc README.rst
%if %{pyver} == 2
%doc html
%endif
%{pyver_sitelib}/%{src_name}
%{pyver_sitelib}/*.egg-info
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/plugins/ml2/*.ini

%changelog
