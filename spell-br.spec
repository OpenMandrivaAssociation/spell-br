%define languagelocal	brezhoneg
%define languageeng	breton
%define languagecode	br
%define languageenglazy Breton
%define lc_ctype	br_FR
%define DIC	 %{languagelocal}.dic

%define spell_group System/Internationalization

Name: 		spell-%{languagecode} 
Version: 	0.2.1
Release: 	%mkrel 8
Summary: 	Breton files for ispell and aspell
Group: 		%{spell_group}
URL: 		http://www.mandrake-linux.com
Source:		spell-br-%{version}.tar.bz2
License: 	GPL
BuildRoot: 	%{_tmppath}/%{name}-buildroot
Prefix: 	%{_prefix}
Autoreqprov:   no
BuildRequires:	locales-%{languagecode}
BuildRequires: aspell ispell

%description -n spell-%{languagecode}
Spell-br is a set of breton dictionnaries for {a,i}spell.


%package -n ispell-%{languagecode}
Summary: 	Breton files for ispell
Group: 		%{spell_group}
Requires:	locales-%{languagecode} ispell
Provides:	ispell-dictionary, ispell-bzh

%description -n ispell-%{languagecode}
Ispell-br is spelling data in Breton to be used by ispell program.
With this extension, you can compose a document in Breton and check
for the typos easily.
Ispell can be used directly from command line to check a file; 
or used by several text dealing programs, like LyX, etc.

To check spelling in brezhoneg text (Latin1 aka ISO-8859 -
though the C'H and CH letters are not present in Latin1 :-) )
Use command:
ispell -d brezhoneg <file_name>

%description -n ispell-%{languagecode} -l br
Geriadur brezhonek evit ispell.

%description -n ispell-%{languagecode} -l fr
Ceci est le dictionnaire breton pour le correcteur orthographique
interactif GNU ispell.




%package -n aspell-%{languagecode}
Summary:	%{languageenglazy} files for aspell
Group:		%{spell_group}
License:	GPL
Requires:	locales-%{languagecode} aspell
Provides:	aspell-dictionary
ExcludeArch:	ia64
Autoreqprov:	no

%description -n aspell-br
A %{languageenglazy} dictionary for use with aspell, a spelling checker.

%prep
%setup -q -n spell-%{languagecode}-%{version}

%build
echo Demad douar
buildhash %{DIC} brezhoneg.aff brezhoneg.hash

# Aspell build
cp %{_datadir}/aspell/iso8859-1.dat .
cat %{DIC}| ispell -e -d ./%{languagelocal}| tr ' ' '\n' > %{languagelocal}.aspell

#cat %{languagelocal}.aspell | word-list-compress compress|\
LC_CTYPE=%{lc_ctype} aspell --lang=%{languagelocal} --data-dir=. \
	create master ./%{languagelocal} < %{languagelocal}.aspell


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{%{_libdir}/aspell,%{_prefix}/lib/ispell,%{_datadir}/{aspell,pspell}}

install -m 644 %{languagelocal}.aff $RPM_BUILD_ROOT%{_prefix}/lib/ispell/%{languagelocal}.aff
install -m 644 %{languagelocal}.hash $RPM_BUILD_ROOT%{_prefix}/lib/ispell/%{languagelocal}.hash

# LaTeX babel
if [ "%{languagelocal}" != "%{languageeng}" ];then
	pushd $RPM_BUILD_ROOT%{_prefix}/lib/ispell
	ln -s %{languagelocal}.aff %{languageeng}.aff
	ln -s %{languagelocal}.hash %{languageeng}.hash
	popd
fi

#	Aspell stuff
install -m 0644 %{languagelocal} $RPM_BUILD_ROOT%{_libdir}/aspell
install -m 0644 %{languagelocal}.dat $RPM_BUILD_ROOT%{_datadir}/aspell

[ -e %{languagelocal}_phonet.dat ]&& install -m 0644 %{languagelocal}_phonet.dat $RPM_BUILD_ROOT/usr/share/aspell

echo "%{_libdir}/aspell/%{languagelocal}" > $RPM_BUILD_ROOT%{_datadir}/pspell/%{languagecode}-aspell.pwli

if [ "%{languagelocal}" != "%{languageeng}" ];then
	(cd $RPM_BUILD_ROOT%{_libdir}/aspell; ln -s %{languagelocal} %{languageeng})
	(cd $RPM_BUILD_ROOT%{_datadir}/aspell; ln -s %{languagelocal}.dat %{languageeng}.dat)
	[ -e %{languagelocal}_phonet.dat ] && ln -s %{languagelocal}_phonet.dat %{languageeng}_phonet.dat
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files -n ispell-br
%defattr(644, root, root,755)
%doc docs/*
%{_prefix}/lib/ispell/*

%files -n aspell-br
%defattr(-,root,root)
%doc docs/*
%{_datadir}/aspell/*
%{_libdir}/aspell/*
%{_datadir}/pspell/*

