# Todo: build docs
# BuildRequires:  gtk-doc >= 1.14
# configure --enable-gtk-doc --enable-gtk-doc-html --enable-gtk-doc-pdf

%global ubuntu_release 16.04

# Set to 1 to run testsuite
%global with_tests 0

Name:       libdbusmenu
Version:    %{ubuntu_release}.0
Release:    4%{?dist}
Summary:    Library for passing menus over DBus

# All files installed in final rpms use C sources with dual licensing headers.
# Tests compiled in the build process are licensed GPLv3

License:    LGPLv3 or LGPLv2 and GPLv3
URL:        https://launchpad.net/libdbusmenu
Source0:    https://launchpad.net/libdbusmenu/%{ubuntu_release}/%{version}/+download/%{name}-%{version}.tar.gz

BuildRequires:  atk-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gettext
BuildRequires:  glibc-devel
BuildRequires:  gnome-common
BuildRequires:  gnome-doc-utils
BuildRequires:  intltool
BuildRequires:  libtool
BuildRequires:  libxslt
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(atk)
BuildRequires:  pkgconfig(gio-2.0) >= 2.35.4
BuildRequires:  pkgconfig(gio-unix-2.0) >= 2.24
BuildRequires:  pkgconfig(glib-2.0) >= 2.35.4
BuildRequires:  pkgconfig(gobject-introspection-1.0) >= 0.10
BuildRequires:  pkgconfig(gtk+-2.0) >= 2.16
BuildRequires:  pkgconfig(gtk+-3.0) >= 2.91
BuildRequires:  pkgconfig(json-glib-1.0) >= 0.13.4
BuildRequires:  pkgconfig(x11) >= 1.3
BuildRequires:  python
BuildRequires:  vala-devel
BuildRequires:  vala-tools

# pkgconfig file is checked for valgrind, but is actually only used for tests
# https://bugzilla.redhat.com/show_bug.cgi?id=1262274
# BuildRequires:  pkgconfig(valgrind)
%if 0%{?with_tests}
BuildRequires:  dbus-test-runner
BuildRequires:  valgrind
%endif

%description
This is a small library designed to make sharing and displaying of menu
structures over DBus simple and easy to use. It works for both QT and GTK+ and
makes building menus simple.

%package devel
Summary:    %{summary} - Development files
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   dbus-glib-devel

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package gtk2
Summary:    %{summary} - GTK+2 version
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description gtk2
Shared libraries for the %{name}-gtk2 library.

%package gtk3
Summary:    %{summary} - GTK+3 version
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description gtk3
Shared libraries for the %{name}-gtk3 library.

%package gtk2-devel
Summary:    Development files for %{name}-gtk2
Requires:   %{name}-gtk2%{?_isa} = %{version}-%{release}
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   gtk2-devel
Requires:   dbus-glib-devel

%description gtk2-devel
The %{name}-gtk2-devel package contains libraries and header files for
developing applications that use %{name}-gtk2.

%package gtk3-devel
Summary:    Development files for %{name}-gtk3
Requires:   %{name}-gtk3%{?_isa} = %{version}-%{release}
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   gtk3-devel
Requires:   dbus-glib-devel

%description gtk3-devel
The %{name}-gtk3-devel package contains libraries and header files for
developing applications that use %{name}-gtk3.

%package jsonloader
Summary:    Test lib development files
Requires:   %{name}-devel%{?_isa} = %{version}-%{release}
Requires:   libdbusmenu = %{version}-%{release}

%description jsonloader
Test library for %{name}.

%package jsonloader-devel
Summary:    Test lib development files for %{name}
Requires:   %{name}-jsonloader%{?_isa} = %{version}-%{release}
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description jsonloader-devel
The %{name}-jsonloader-devel package contains libraries and header files for
developing applications that use %{name}-jsonloader.

%package    doc
Summary:    Document files for %{name}
BuildArch:  noarch

%description doc
The %{name}-doc package contains documents for developing applications that
use %{name}.

%package    tools
Summary:    Development tools for the dbusmenu libraries
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description tools
The %{name}-tools package contains helper tools for developing applications
that use %{name}.


%prep
%setup -q -n %{name}-%{version} -c
cp -a %{name}-%{version}/{README,COPYING,COPYING.2.1,COPYING-GPL3,AUTHORS,ChangeLog} .
cp -a %{name}-%{version} %{name}-gtk3-%{version}


%build
build(){
autoreconf -vif
%configure --disable-static --disable-dumper $*
%make_build
}

pushd %{name}-gtk3-%{version}
sed -i -e 's@^#!.*python$@#!/usr/bin/python2@' tools/dbusmenu-bench
build --with-gtk=3
popd

pushd %{name}-%{version}
sed -i -e 's@^#!.*python$@#!/usr/bin/python2@' tools/dbusmenu-bench
build --with-gtk=2
popd


%install
pushd %{name}-gtk3-%{version}
%make_install
find %{buildroot} -name '*.la' -delete
popd

pushd %{name}-%{version}
%make_install
find %{buildroot} -name '*.la' -delete
popd

# Let rpmbuild pick the documents in the files section
rm -fr %{buildroot}%{_docdir}/%{name}

%if 0%{?with_tests}
%check
for variant in %{name}-gtk3-%{version} %{name}-%{version}; do
    pushd $variant
        make check V=1
    popd
done
%endif

%post -p /sbin/ldconfig
%post gtk2 -p /sbin/ldconfig
%post gtk3 -p /sbin/ldconfig
%post jsonloader -p /sbin/ldconfig

%postun -p /sbin/ldconfig
%postun gtk2 -p /sbin/ldconfig
%postun gtk3 -p /sbin/ldconfig
%postun jsonloader -p /sbin/ldconfig

%files
%license COPYING COPYING.2.1 COPYING-GPL3
%doc README AUTHORS ChangeLog
%{_libdir}/libdbusmenu-glib.so.*
%{_libdir}/girepository-1.0/Dbusmenu-0.4.typelib

%files devel
%doc %{name}-%{version}/tests/glib-server-nomenu.c
%dir %{_includedir}/libdbusmenu-glib-0.4/
%dir %{_includedir}/libdbusmenu-glib-0.4/libdbusmenu-glib/
%{_includedir}/libdbusmenu-glib-0.4/libdbusmenu-glib/*.h
%{_libdir}/libdbusmenu-glib.so
%{_libdir}/pkgconfig/dbusmenu-glib-0.4.pc
%{_datadir}/gir-1.0/Dbusmenu-0.4.gir
%{_datadir}/vala/vapi/Dbusmenu-0.4.vapi

%files jsonloader
%{_libdir}/libdbusmenu-jsonloader.so.*

%files jsonloader-devel
%dir %{_includedir}/libdbusmenu-glib-0.4/
%dir %{_includedir}/libdbusmenu-glib-0.4/libdbusmenu-jsonloader/
%{_includedir}/libdbusmenu-glib-0.4/libdbusmenu-jsonloader/*.h
%{_libdir}/libdbusmenu-jsonloader.so
%{_libdir}/pkgconfig/dbusmenu-jsonloader-0.4.pc

%files gtk3
%{_libdir}/libdbusmenu-gtk3.so.*
%{_libdir}/girepository-1.0/DbusmenuGtk3-0.4.typelib

%files gtk2
%{_libdir}/libdbusmenu-gtk.so.*
%{_libdir}/girepository-1.0/DbusmenuGtk-0.4.typelib

%files gtk3-devel
%dir %{_includedir}/libdbusmenu-gtk3-0.4
%dir %{_includedir}/libdbusmenu-gtk3-0.4/libdbusmenu-gtk
%{_includedir}/libdbusmenu-gtk3-0.4/libdbusmenu-gtk/*.h
%{_libdir}/libdbusmenu-gtk3.so
%{_libdir}/pkgconfig/dbusmenu-gtk3-0.4.pc
%{_datadir}/gir-1.0/DbusmenuGtk3-0.4.gir
%{_datadir}/vala/vapi/DbusmenuGtk3-0.4.vapi

%files gtk2-devel
%dir %{_includedir}/libdbusmenu-gtk-0.4
%dir %{_includedir}/libdbusmenu-gtk-0.4/libdbusmenu-gtk
%{_includedir}/libdbusmenu-gtk-0.4/libdbusmenu-gtk/*.h
%{_libdir}/libdbusmenu-gtk.so
%{_libdir}/pkgconfig/dbusmenu-gtk-0.4.pc
%{_datadir}/gir-1.0/DbusmenuGtk-0.4.gir
%{_datadir}/vala/vapi/DbusmenuGtk-0.4.vapi

%files doc
%dir %{_datadir}/gtk-doc/
%{_datadir}/gtk-doc/*

%files tools
%doc %{name}-%{version}/tools/README.dbusmenu-bench
%{_libexecdir}/dbusmenu-bench
%{_libexecdir}/dbusmenu-testapp
%dir %{_datadir}/%{name}/
%dir %{_datadir}/%{name}/json/
%{_datadir}/%{name}/json/test-gtk-label.json

%changelog
* Mon Feb 26 2018 Tomas Popela <tpopela@redhat.com> - 16.04.0-4
- Fix rpmdiff warning
- Resolves: rhbz#1546660

* Tue Feb 20 2018 Tomas Popela <tpopela@redhat.com> - 16.04.0-3
- Move package from EPEL 7 to RHEL 7
- Resolves: rhbz#1546660

* Mon Apr 17 2017 Simone Caronni <negativo17@gmail.com> - 16.04.0-2
- Add tests, remove valgrind-devel build requirements (#1262274).
- Disable tests until dbus-test-runner is available.

* Sun Apr 16 2017 Simone Caronni <negativo17@gmail.com> - 16.04.0-1
- Update to 16.04.0.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.10.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.10.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 12.10.2-7
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.10.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 26 2013 Eduardo Echeverria <echevemaster@gmail.com> - 12.10.2-5
- switch to unversioned documentation directory

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.10.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jun 02 2013 Dan Horák <dan[at]danny.cz> - 12.10.2-3
- valgrind exists only on selected arches

* Mon May 27 2013 Eduardo Echeverria <echevemaster@gmail.com> - 12.10.2-2
- Fix issues with macros-in-comment
- Fix cosmetics errors
- Workaround for the docs files
- Fix a issue with the ownership of the some directories

* Sun Feb 17 2013 Eduardo Echeverria <echevemaster@gmail.com> - 12.10.2-1
- initial packaging
