%define name    ape
%define version 1.1.2
%define release %mkrel 1
%define revision 0eff8f0

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:    	A full-featured OpenSource solution designed for Ajax Push
License:    	GPLv2+
Group:      	Networking/Other
URL:        	http://www.ape-project.org/
Source:     	APE-Project-APE_Server-v1.1.0-14-g0eff8f0.tar.gz
Source1:     	ape.sysconfig
Source2:     	ape.init
Patch0:		ape-makefile.patch
Patch1:		ape-conf.patch
BuildRequires:	mysql-devel
BuildRequires:	js-devel
BuildRequires:	udns-devel
BuildRequires:	mysac-devel
BuildRoot:  	%{_tmppath}/%{name}-%{version}

%description
A full-featured OpenSource solution designed for Ajax Push. It includes a 
webserver and a Javascript Framework. APE allows to implement any kind of 
real-time data streaming to a web browser, without having to install 
anything on the client-side 

%prep
%setup -q -n APE-Project-APE_Server-%{revision}
%patch0 -p1 -b .makefile
%patch1 -p1 -b .conf

cat bin/ape.conf|sed -r 's|/usr/lib|%{_libdir}|' >  ape.conf.1
%{__rm} -f bin/imspector.conf
mv ape.conf.1 bin/ape.conf

cat Makefile|sed -r 's|/usr/lib|%{_libdir}|' >  Makefile.1
%{__rm} -f Makefile
mv Makefile.1 Makefile

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
%{__install} -d %{buildroot}%{_libdir}/ape
%{__install} modules/lib/libmod_spidermonkey.so %{buildroot}%{_libdir}/ape
%{__mkdir_p}  %{buildroot}%{_var}/log/ape
%{__mkdir_p} %{buildroot}%{_initrddir}
%{__mkdir_p} %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -m0755 %{SOURCE2} %{buildroot}%{_initrddir}/ape
%{__install} -m0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/ape
echo scripts_path = %{_docdir}/ape/ > %{buildroot}%{_sysconfdir}/ape/javascript.conf


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
%{_sysconfdir}/ape/ape.conf
%{_sysconfdir}/ape/javascript.conf
%_sbindir/*
%{_libdir}/ape/*

