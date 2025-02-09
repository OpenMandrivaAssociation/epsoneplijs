Summary:	Ghostscript IJS Plugin for the Epson EPL-5700L/5800L/5900L/6100L/6200L printers
Name:		epsoneplijs
Version:	0.4.1
Release:	21
Group:		System/Printing
License:	BSD
Url:		https://sourceforge.net/projects/epsonepl/
Source0:	http://osdn.dl.sourceforge.net/sourceforge/epsonepl/epsoneplijs-%{version}.tgz
Patch0:		epsoneplijs-use_system_libs.diff
Patch1:		epsoneplijs-mandriva-install.diff
Patch2:		epsoneplijs-0.4.1-LDFLAGS.diff

BuildRequires:	libtool
BuildRequires:	ieee1284-devel
BuildRequires:	pkgconfig(libusb)
Requires:	ghostscript >= 6.53

%description
Support for the Epson EPL-5700L/5800L/5900L/6100L/6200L printer family under
linux and other unix-like systems.
It is known to work for at least one user for each of 5700L, 5800L,
5900L, and 6100L. 6100L and 6200L support is new.

%prep
%setup -q
%autopatch -p1

sed -i -e "s|-g -O2 -Wall -Werror -ansi -pedantic -Wmissing-prototypes|$CFLAGS -fPIC|g" Makefile.in

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
	if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

autoreconf -fi

%build
%serverbuild
%configure2_5x \
	--with-kernelusb \
	--with-kernel1284 \
	--with-libusb \
	--with-libieee1284 

%make
%make test5700lusb

gcc $CFLAGS -fPIC -Wall %{ldflags} -o epl-5700 epl_docs/epl-5700.c
gcc $CFLAGS -fPIC -Wall %{ldflags} -o epl-5800 epl_docs/epl-5800.c
gcc $CFLAGS -fPIC -Wall %{ldflags} -o epl5x00l epl_docs/epl5x00l.c

%install
install -d %{buildroot}%{_bindir}
%makeinstall

install -m0755 ps2epl.pl %{buildroot}%{_bindir}
install -m0755 test5700lusb %{buildroot}%{_bindir}/
install -m0755 epl-5700 %{buildroot}%{_bindir}/
install -m0755 epl-5800 %{buildroot}%{_bindir}/
install -m0755 epl5x00l %{buildroot}%{_bindir}/

pushd foomatic_scripts
sh install_mandrake %{buildroot}
popd

%files
%doc ChangeLog FAQ LIMITATIONS README* *.pdf epl_test* apsfilter cups epl_docs/epl-protocol.pdf epl_docs/README.1st
%{_bindir}/*
%{_datadir}/cups/model/epson/*.ppd.gz
%{_datadir}/foomatic/db/source/driver/*.xml
%{_datadir}/foomatic/db/source/opt/*.xml

