%define name		xjavadoc
%define version		1.1
%define release		1.6
%define section		free
%define gcj_support	1

Name:		%{name}
Version:	%{version}
Release:	%mkrel %{release}
Epoch:		0
Summary:	The XJavaDoc engine
License:	BSD Style
URL:		http://xdoclet.sourceforge.net/xjavadoc/
Group:		Development/Java
Source0:	%{name}-src-%{version}-RHCLEAN.tar.bz2
# cvs -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/xdoclet login
# cvs -z3 -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/xdoclet export -r XJAVADOC_1_1 xjavadoc
Patch0:		%{name}-build_xml.patch
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
Requires:	jakarta-commons-logging
Requires:	jakarta-commons-collections
Requires:	xml-commons-jaxp-1.3-apis
Requires:	log4j
Requires:	xalan-j2
Requires:	jrefactory
%if %{gcj_support}
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat
BuildRequires:  java-gcj-compat-devel
%else
Buildarch:      noarch
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
rm -rf $RPM_BUILD_ROOT
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

%clean
rm -rf $RPM_BUILD_ROOT

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


