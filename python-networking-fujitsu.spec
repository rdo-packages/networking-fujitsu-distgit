%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global plugin_name networking-fujitsu
%global src_name networking_fujitsu

%global common_desc \
This package contains Fujitsu neutron plugins

Name:           python-%{plugin_name}
Version:        6.0.0
Release:        1%{?dist}
Summary:        FUJITSU ML2 plugins/drivers for OpenStack Neutron
License:        ASL 2.0
URL:            https://pypi.python.org/pypi/%{plugin_name}
Source0:        https://tarballs.openstack.org/%{plugin_name}/%{plugin_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

BuildRequires:  git
BuildRequires:  python2-hacking
BuildRequires:  python2-subunit
BuildRequires:  python2-sphinx
BuildRequires:  python2-oslo-sphinx
BuildRequires:  python2-oslotest
BuildRequires:  python2-testrepository
BuildRequires:  python2-testscenarios
BuildRequires:  python2-testtools
BuildRequires:  python2-reno
BuildRequires:  python2-testresources
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-oslo-i18n
BuildRequires:  python2-oslo-utils
BuildRequires:  openstack-neutron
BuildRequires:  python-neutron-tests
BuildRequires:  python2-mock
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python2-%{plugin_name}
Summary:  neutron ML2 plugin for Fujitsu switch
%{?python_provide:%python_provide python2-%{plugin_name}}

Requires:       python2-oslo-i18n >= 3.15.3
Requires:       python2-oslo-utils >= 3.33.0
Requires:       python2-oslo-log >= 3.36.0
Requires:       python2-pbr >= 1.8
Requires:       python2-six
Requires:       openstack-neutron-common
Requires:       openstack-neutron-ml2
Requires:       python2-oslo-config
Requires:       python2-eventlet

%description -n python2-%{plugin_name}
%{common_desc}

%prep
%autosetup -n %{plugin_name}-%{upstream_version} -S git
%py_req_cleanup

%build
%py2_build
sphinx-build doc/source html
rm -rf html/.{doctrees,buildinfo}

%install
%py2_install
install -d -m 755 %{buildroot}%{_sysconfdir}/neutron/plugins/ml2/
mv %{buildroot}/usr/etc/neutron/plugins/ml2/*.ini %{buildroot}%{_sysconfdir}/neutron/plugins/ml2/

%check
%{__python2} setup.py test

%files -n python2-%{plugin_name}
%license LICENSE
%doc README.rst
%doc html
%{python2_sitelib}/%{src_name}
%{python2_sitelib}/*.egg-info
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/plugins/ml2/*.ini

%changelog
* Tue Feb 20 2018 RDO <dev@lists.rdoproject.org> 6.0.0-1
- Update to 6.0.0

 * Fri Dec 02 2016 Koki Sanagi<sanagi.koki@jp.fujitsu.com> - 2.0.0-1
 - Initial package.
