%define revision 0eff8f0

Name:		ape
Version:	1.1.2
Release:	9
Summary:    	A full-featured OpenSource solution designed for Ajax Push
License:    	GPLv2+
Group:      	Networking/Other
URL:        	http://www.ape-project.org/
Source:     	APE-Project-APE_Server-v1.1.0-14-g0eff8f0.tar.gz
Source1:     	ape.sysconfig
Source2:     	ape.init
Source3:	http://www.ape-project.org/stable/APE_JSF-1.1.0.tar.gz
Patch0:		ape-makefile.patch
Patch1:		ape-conf.patch
BuildRequires:	mysql-devel
BuildRequires:	js-devel
BuildRequires:	udns-devel
BuildRequires:	mysac-devel
BuildRequires:  tar
BuildRequires:  gzip

%description
A full-featured OpenSource solution designed for Ajax Push. It includes a 
webserver and a Javascript Framework. APE allows to implement any kind of 
real-time data streaming to a web browser, without having to install 
anything on the client-side 

%package        www
Summary:        APE frontend
Group:          Networking/Other
Suggests:       %{name}
Requires:       webserver

%description    www
This package let comunication between APE and apache


%prep
%setup -q -n APE-Project-APE_Server-%{revision}
%patch0 -p1 -b .makefile
%patch1 -p1 -b .conf

cat bin/ape.conf|sed -r 's|/usr/lib|%{_libdir}|' >  ape.conf.1
%{__rm} -f bin/ape.conf
mv ape.conf.1 bin/ape.conf

cat Makefile|sed -r 's|/usr/lib|%{_libdir}|' >  Makefile.1
%{__rm} -f Makefile
mv Makefile.1 Makefile

%if %mdkversion < 201100
cat modules/Makefile|sed -r 's|mysqld|mysqlclient|' >  Makefile.1
%{__rm} -f modules/Makefile
mv Makefile.1 modules/Makefile

%endif


echo "HAS_MYSQL = yes" > ./modules/mysql.mk
echo "#define USE_EPOLL_HANDLER" > ./src/configure.h
echo "LINUX_BUILD = 1" > ./modules/plateform.mk
echo "#define _USE_MYSQL 1" >> ./src/configure.h

%make
# "CFLAGS=%optflags"
cd modules
%make  LIBDIR=%{_libdir}

%install
%makeinstall
%{__install} -d %{buildroot}%{_sysconfdir}/ape
%{__install} bin/ape.conf %{buildroot}%{_sysconfdir}/ape
%{__install} modules/conf/inlinepush.conf %{buildroot}%{_sysconfdir}/ape
%{__install} modules/conf/proxy.conf %{buildroot}%{_sysconfdir}/ape
%{__install} -d %{buildroot}%{_libdir}/ape
%{__install} modules/lib/libmod_spidermonkey.so %{buildroot}%{_libdir}/ape
%{__mkdir_p}  %{buildroot}%{_var}/log/ape
%{__mkdir_p} %{buildroot}%{_initrddir}
%{__mkdir_p} %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -m0755 %{SOURCE2} %{buildroot}%{_initrddir}/ape
%{__install} -m0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/ape
echo scripts_path = %{_docdir}/ape/ > %{buildroot}%{_sysconfdir}/ape/javascript.conf
# provide a simple apache config
%{__mkdir_p} %{buildroot}%{_sysconfdir}/httpd/conf/vhosts.d/
cat > %{buildroot}%{_sysconfdir}/httpd/conf/vhosts.d/99_ape.conf << EOF
<VirtualHost *>
        Servername localhost
        ServerAlias ape.*
        ServerAlias *.ape.*
 
        DocumentRoot "/var/www/ape/"
</VirtualHost>

<Directory /var/www/ape/>
    Options -Indexes FollowSymLinks MultiViews
    AllowOverride None
    Order allow,deny
    Allow from all
</Directory>
EOF

%{__mkdir_p} %{buildroot}%{_var}/www/ape/
pushd %{buildroot}%{_var}/www/ape/
tar -zxvf %{SOURCE3} 
popd

%clean
%{__rm} -rf %{buildroot}


%preun
%_preun_service ape

%pre
%_pre_useradd ape %{_libdir}/ape /bin/false

%postun
%_postun_userdel ape
%_postun_groupdel ape



%post
%_post_service ape



%files
%defattr(-,root,root)
%doc scripts/*
%dir %{_sysconfdir}/ape/
%dir %{_libdir}/ape/
%dir %{_var}/log/ape
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/ape
%attr(0755,root,root) %{_initrddir}/ape
%config(noreplace) %{_sysconfdir}/ape/ape.conf
%config(noreplace) %{_sysconfdir}/ape/javascript.conf
%config(noreplace) %{_sysconfdir}/ape/inlinepush.conf
%config(noreplace) %{_sysconfdir}/ape/proxy.conf
%_sbindir/*
%{_libdir}/ape/*

%files www
%dir %{_var}/www/ape/
%config(noreplace) %{_sysconfdir}/httpd/conf/vhosts.d/99_ape.conf
%{_var}/www/ape/*


%changelog
* Wed Jun 29 2011 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 1.1.2-6mdv2011.0
+ Revision: 688241
- SPEC fixes and missing conf files

* Mon Jun 27 2011 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 1.1.2-5
+ Revision: 687388
- apache macros

* Mon Jun 27 2011 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 1.1.2-4
+ Revision: 687385
- www subpackage to communicate with apache

* Sun Jun 26 2011 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 1.1.2-3
+ Revision: 687381
- init script fixes
- mysql 5.1 support

* Sun Jun 26 2011 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 1.1.2-2
+ Revision: 687270
- lib64 support
- import ape

