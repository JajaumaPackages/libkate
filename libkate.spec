%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           libkate
Version:        0.3.3
Release:        2%{?dist}
Summary:        Libraries to handle the Kate bitstream format

Group:          System Environment/Libraries
License:        BSD
URL:            http://code.google.com/p/libkate/
Source0:        http://libkate.googlecode.com/files/libkate-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel
BuildRequires:  libogg-devel
BuildRequires:  liboggz
BuildRequires:  libpng-devel
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  valgrind
BuildRequires:  doxygen
 

%description
This is libkate, the reference implementation of a codec for the Kate bitstream
format.
Kate is a karaoke and text codec meant for encapsulation in an Ogg container.
It can carry text, images, and animate them.

Kate is meant to be used for karaoke alongside audio/video streams (typically
Vorbis and Theora), movie subtitles, song lyrics, and anything that needs text
data at arbitrary time intervals.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       libogg-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package utils
Summary:        Encoder/Decoder utilities for %{name}
Group:          Applications/Multimedia
Requires:       %{name} = %{version}-%{release}
Requires:       liboggz

%description utils
The %{name}-utils package contains the katedec/kateenc binaries for %{name}.

%package docs
Summary:        Documentation for %{name}
Group:          Documentation
BuildArch:      noarch

%description docs
The %{name}-docs package contains the docs for %{name}.


%prep
%setup -q

# We regenerate theses files at built step
rm tools/kate_parser.{c,h}
rm tools/kate_lexer.c


%build
%configure --disable-static \
  --docdir=%{_docdir}/%{name}-%{version}

# Remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# Fix for header timestramps
touch -r $RPM_BUILD_ROOT%{_includedir}/kate/kate_config.h \
 $RPM_BUILD_ROOT%{_includedir}/kate/kate.h


%check
make check


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%exclude %{_docdir}/libkate-%{version}/html
%doc %{_docdir}/libkate-%{version}
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc examples/
%{_includedir}/kate/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files utils
%defattr(-,root,root,-)
%{python_sitelib}/kdj/
%{_bindir}/KateDJ
%{_bindir}/katalyzer
%{_bindir}/katedec
%{_bindir}/kateenc
%{_mandir}/man1/KateDJ.*
%{_mandir}/man1/katalyzer.*
%{_mandir}/man1/katedec.*
%{_mandir}/man1/kateenc.*

%files docs
%defattr(-,root,root,-)
%doc %{_docdir}/libkate-%{version}/html


%changelog
* Mon Jun 29 2009 kwizart < kwizart at gmail.com > - 0.3.3-2
- Split -docs - Fix #508589

* Mon May 11 2009 kwizart < kwizart at gmail.com > - 0.3.3-1
- Update to 0.3.3

* Fri Apr 10 2009 kwizart < kwizart at gmail.com > - 0.3.1-3
- Use Fedora compliant (using version) _docdir directory.
- Remove shebangs when not needed.
- Bundle examples within -devel
- Use global instead of define

* Sat Apr  4 2009 kwizart < kwizart at gmail.com > - 0.3.1-2
- Prevent conflict with GNU getline() in recent rawhide

* Tue Mar 17 2009 kwizart < kwizart at gmail.com > - 0.3.1-1
- Update to 0.3.1

* Tue Jan 13 2009 kwizart < kwizart at gmail.com > - 0.3.0-1
- Update to 0.3.0
- Add KateDJ and katalyzer in -utils
- Add BR liboggz and -utils Requires liboggz

* Wed Nov 27 2008 kwizart < kwizart at gmail.com > - 0.2.7-1
- Update to 0.2.7

* Mon Oct 20 2008 kwizart < kwizart at gmail.com > - 0.2.5-1
- Update to 0.2.5

* Mon Sep 29 2008 kwizart < kwizart at gmail.com > - 0.2.1-1
- Update to 0.2.1

* Thu Sep 11 2008 kwizart < kwizart at gmail.com > - 0.1.12-1
- Update to 0.1.12

* Thu Sep  4 2008 kwizart < kwizart at gmail.com > - 0.1.11-1
- Update to 0.1.11

* Wed Sep  3 2008 kwizart < kwizart at gmail.com > - 0.1.10-1
- Update to 0.1.10

* Tue Sep  2 2008 kwizart < kwizart at gmail.com > - 0.1.9-1
- Update to 0.1.9

* Fri Aug 29 2008 kwizart < kwizart at gmail.com > - 0.1.8-1
- Update to 0.1.8

* Mon Aug 11 2008 kwizart < kwizart at gmail.com > - 0.1.7-1
- Initial spec file
