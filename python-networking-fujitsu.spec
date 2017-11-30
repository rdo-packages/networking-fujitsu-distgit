%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global plugin_name networking-fujitsu
%global src_name networking_fujitsu

Name:           python-%{plugin_name}
Version:        5.0.1
Release:        1%{?dist}
Summary:        FUJITSU ML2 plugins/drivers for OpenStack Neutron
License:        ASL 2.0
URL:            https://pypi.python.org/pypi/%{plugin_name}
Source0:        https://tarballs.openstack.org/%{plugin_name}/%{plugin_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

BuildRequires:  git
BuildRequires:  python-hacking
BuildRequires:  python-subunit
BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-oslotest
BuildRequires:  python-testrepository
BuildRequires:  python-testscenarios
BuildRequires:  python-testtools
BuildRequires:  python-reno
BuildRequires:  python-testresources
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-oslo-i18n
BuildRequires:  python-oslo-utils
BuildRequires:  openstack-neutron
BuildRequires:  python-neutron-tests
BuildRequires:  python-mock

%description
This package contains Fujitsu neutron plugins

%package -n python2-%{plugin_name}
Summary:  neutron ML2 plugin for Fujitsu switch
%{?python_provide:%python_provide python2-%{plugin_name}}

Requires:       python-oslo-i18n >= 2.1.0
Requires:       python-oslo-utils >= 3.16.0
Requires:       python-oslo-log >= 3.11.0
Requires:       python-pbr >= 1.8
Requires:       python-babel >= 2.3.4
Requires:       python-six
Requires:       openstack-neutron-common
Requires:       openstack-neutron-ml2
Requires:       python-oslo-config
Requires:       python-eventlet
Requires:       python-httplib2

%description -n python2-%{plugin_name}
This package contains Fujitsu neutron plugins

%prep
%autosetup -n %{plugin_name}-%{upstream_version} -S git
rm -rf {test-,}requirements.txt

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
* Thu Nov 30 2017 Yasuyuki Kobayashi <kobayash.yasu@jp.fujitsu.com> 5.0.1-1
- Update to 5.0.1

* Wed Aug 30 2017 Haikel Guemar <hguemar@fedoraproject.org> 4.1.2-1
- Update to 4.1.2

 * Fri Dec 02 2016 Koki Sanagi<sanagi.koki@jp.fujitsu.com> - 2.0.0-1
 - Initial package.

