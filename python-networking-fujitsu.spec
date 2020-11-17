
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

BuildRequires:  git-core
BuildRequires:  python3-hacking
BuildRequires:  python3-subunit
BuildRequires:  python3-sphinx
BuildRequires:  python3-oslo-sphinx
BuildRequires:  python3-oslotest
BuildRequires:  /usr/bin/stestr-3
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools
BuildRequires:  python3-reno
BuildRequires:  python3-testresources
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-oslo-i18n
BuildRequires:  python3-oslo-utils
BuildRequires:  openstack-neutron
BuildRequires:  python3-neutron-tests
BuildRequires:  python3-neutron-lib-tests
BuildRequires:  python3-mock
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python3-%{plugin_name}
Summary:  neutron ML2 plugin for Fujitsu switch
%{?python_provide:%python_provide python3-%{plugin_name}}

Requires:       python3-oslo-i18n >= 3.15.3
Requires:       python3-oslo-utils >= 3.33.0
Requires:       python3-oslo-log >= 3.36.0
Requires:       python3-pbr >= 2.0.0
Requires:       python3-six
Requires:       openstack-neutron-common >= 1:13.0.0
Requires:       openstack-neutron-ml2 >= 1:13.0.0
Requires:       python3-oslo-config
Requires:       python3-eventlet
Requires:       python3-neutron-lib >= 1.18.0
Requires:       python3-paramiko >= 2.0.0

%description -n python3-%{plugin_name}
%{common_desc}

%prep
%autosetup -n %{plugin_name}-%{upstream_version} -S git
%py_req_cleanup

%build
%{py3_build}

# oslosphinx do not work with sphinx > 2
#sphinx-build-3 -W -b html doc/source html
#rm -rf html/.{doctrees,buildinfo}

%install
%{py3_install}
install -d -m 755 %{buildroot}%{_sysconfdir}/neutron/plugins/ml2/
mv %{buildroot}/usr/etc/neutron/plugins/ml2/*.ini %{buildroot}%{_sysconfdir}/neutron/plugins/ml2/

%check
export PYTHON=%{__python3}
stestr run --test-path %{src_name}/tests/unit run

%files -n python3-%{plugin_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{src_name}
%{python3_sitelib}/*.egg-info
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/plugins/ml2/*.ini

%changelog
