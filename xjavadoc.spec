%define section		free
%define gcj_support	0

Name:		xjavadoc
Version:	1.1
Release:	1.21
Epoch:		0
Summary:	The XJavaDoc engine
License:	BSD Style
URL:		http://xdoclet.sourceforge.net/xjavadoc/
Group:		Development/Java
Source0:	%{name}-src-%{version}-RHCLEAN.tar.bz2
# cvs -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/xdoclet login
# cvs -z3 -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/xdoclet export -r XJAVADOC_1_1 xjavadoc
Patch0:		%{name}-build_xml.patch
BuildRequires:  java-rpmbuild
BuildRequires:	java
BuildRequires:	java-devel
BuildRequires:	junit
BuildRequires:	ant >= 0:1.5
BuildRequires:	jakarta-commons-logging
BuildRequires:	jakarta-commons-collections
BuildRequires:	xml-commons-jaxp-1.3-apis
BuildRequires:	log4j
BuildRequires:	java-devel 
BuildRequires:	javacc
BuildRequires:	xalan-j2
BuildRequires:	jrefactory
BuildRequires:	ant-junit
BuildRequires:	ant-nodeps
BuildRequires:	locales-en
Requires:	jakarta-commons-logging
Requires:	jakarta-commons-collections
Requires:	xml-commons-jaxp-1.3-apis
Requires:	log4j
Requires:	xalan-j2
Requires:	jrefactory
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
Buildarch:      noarch
%endif

%description
The XJavaDoc engine is a complete rewrite of Sun's 
JavaDoc engine that is faster and more suited for 
XDoclet (although it is completely standalone). It 
scans java source code and makes information about 
a class available via special java beans that are 
part of the XJavaDoc core. These beans provide the 
same information about a class as Sun's JavaDoc API, 
and some nice extra features. 

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description    javadoc
%{summary}.

%prep
%setup -q -n %{name}
find . -name "*.tar.bz2" -exec rm {} \;
find . -name "*.jar" -exec rm {} \;

%patch0 -b .sav

%build
export LC_ALL=ISO-8859-1
export CLASSPATH=$(build-classpath \
xalan-j2 \
junit \
javacc \
log4j \
commons-logging \
commons-collections \
xml-commons-jaxp-1.3-apis \
jrefactory \
ant)

export OPT_JAR_LIST="junit ant/ant-junit ant/ant-nodeps"
%ant -Dbuild.sysclasspath=first -Djavacchome=%{_javadir} javadoc

%install
mkdir -p $RPM_BUILD_ROOT%{_javadir}
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}
mkdir -p $RPM_BUILD_ROOT%{_docdir}
install -m 644 target/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}

# version less symlinks
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

install -d -m 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
install -m 644 LICENSE.txt $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
install -m 644 docs/architecture.txt $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

#javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
    rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(0644,root,root,0755)
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif
%{_docdir}/%{name}-%{version}/*

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}




%changelog
* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.1-1.10mdv2011.0
+ Revision: 608215
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.1-1.9mdv2010.1
+ Revision: 524448
- rebuilt for 2010.1

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 0:1.1-1.8mdv2009.0
+ Revision: 136607
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:1.1-1.8mdv2008.1
+ Revision: 120816
- buildrequires java-rpmbuild

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:1.1-1.7mdv2008.0
+ Revision: 87275
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Thu Jul 26 2007 Anssi Hannula <anssi@mandriva.org> 0:1.1-1.6mdv2008.0
+ Revision: 55962
- use xml-commons-jaxp-1.3-apis explicitely instead of the generic
  xml-commons-apis which is provided by multiple packages (see bug #31473)


* Fri Mar 16 2007 Christiaan Welvaart <spturtle@mandriva.org> 1.1-1.4mdv2007.1
+ Revision: 144765
- rebuild for 2007.1
- Import xjavadoc

* Sun Jun 04 2006 David Walluck <walluck@mandriva.org> 0:1.1-1.2mdv2007.0
- rebuild for libgcj.so.7
- aot-compile

* Sun Sep 11 2005 David Walluck <walluck@mandriva.org> 0:1.1-1.1mdk
- release

* Thu Jun 16 2005 Gary Benson <gbenson@redhat.com> 1.1-1jpp_1fc
- Build into Fedora.

* Thu Jun 09 2005 Gary Benson <gbenson@redhat.com>
- Remove jarfiles and.tar.bz2files from the tarball.

* Tue Jun 07 2005 Gary Benson <gbenson@redhat.com>
- Add build dependency on ant-junit.

* Wed Feb 16 2005 Fernando Nasser <fnasser@redhat.com> 1.1-1jpp_1rh
- Merge with upstream for upgrade

* Tue Feb 15 2005 Ralph Apel <r.apel at r-apel.de> 1.1-1jpp
- upgrade to 1.1
- replace requirement of xml-commons by xml-commons-apis

* Sat Oct 16 2004 Fernando Nasser <fnasser@redhat.com> 1.0.3-2jpp_1rh
- First Red Hat build

* Fri Aug 27 2004 Ralph Apel <r.apel at r-apel.de> 1.0.3-2jpp
- Build with ant-1.6.2

* Sat Jul 03 2004 Ralph Apel <r.apel at r-apel.de> 1.0.3-1jpp
- upgrade to 1.0.3
- just eliminate __GENERATED__ tests because no sources for old xdoclet 
- add xjavadoc javadoc subpackage

