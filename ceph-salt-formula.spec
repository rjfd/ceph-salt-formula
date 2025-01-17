#
# spec file for package ceph-salt-formula
#
# Copyright (c) 2017 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


# See also http://en.opensuse.org/openSUSE:Specfile_guidelines

Name:           ceph-salt-formula
Version:        0.1.0
Release:        1%{?dist}
Summary:        Ceph Salt Formula
Url:            https://github.com/SUSE/ceph-salt-formula
License:        MIT
Group:          System/Management
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%if ! (0%{?sle_version:1} && 0%{?sle_version} < 150100)
Requires(pre):  salt-formulas-configuration
%else
Requires(pre):  salt-master
%endif

%define fname ceph-salt
%define fdir  %{_datadir}/salt-formulas

%description
Salt Formula to deploy Ceph clusters.

%prep
%setup -q -n %{name}-%{version}

%build

%install
mkdir -p %{buildroot}%{fdir}/states/%{fname}/
mkdir -p %{buildroot}%{fdir}/metadata/%{fname}/
cp -R states/* %{buildroot}%{fdir}/states/%{fname}/
cp metadata/* %{buildroot}%{fdir}/metadata/%{fname}/

mkdir -p %{buildroot}%{_datadir}/%{fname}/pillar

# pillar top sls file
cat <<EOF > %{buildroot}%{_datadir}/%{fname}/pillar/top.sls
base:
  '*':
    - ceph-salt
EOF

# empty ceph-salt.sls file
cat <<EOF > %{buildroot}%{_datadir}/%{fname}/pillar/ceph-salt.sls
ceph-salt:

EOF

cat <<EOF > %{buildroot}%{_datadir}/%{fname}/pillar.conf.example
pillar_roots:
  base:
    - /srv/pillar
    - %{_datadir}/%{fname}/pillar
EOF

%files
%defattr(-,root,root,-)
%license LICENSE
%doc README.md
%dir %attr(0755, root, salt) %{fdir}/
%dir %attr(0755, root, salt) %{fdir}/states/
%dir %attr(0755, root, salt) %{fdir}/metadata/
%dir %attr(0755, root, root) %{_datadir}/%{fname}
%{fdir}/states/
%{fdir}/metadata/
%{_datadir}/%{fname}

%changelog