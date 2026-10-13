# prm -- the pixel router software the GMOS OIWFS loads at boot.
#
# The OIWFS crate's startup does
#
#   dbLoadRecords /gemini/epics3.13.4/prm/prm/data/oiwfsPrmTop.db
#   dbLoadRecords /gemini/epics3.13.4/prm/prm/data/oiwfsPrmSadTop.db
#   ld < /gemini/epics3.13.4/prm/prm/bin/ppc604/{prmLib,prmControl,prmtest}
#
# and nothing packaged these files: they existed only on pisces, so a clean
# install of oiwfs would boot and then fail at those lines.
#
# COPY-ONLY, like hrwfs-dhs-vxlibs: the deployed tree (prm -> V2-5.dev,
# unchanged since 2005-2008) shipped verbatim. Its own source is not migrated
# yet. It is kept even though the pixel router has been removed for GMOS-only
# operation, because the OIWFS is expected to serve GNIRS again, and prm is
# how it switches between instruments.

%global _build_id_links none
%global __os_install_post %{nil}
%global debug_package %{nil}
%global _binaries_in_noarch_packages_terminate_build 0
%global prmdir /gemini/epics3.13.4/prm/prm

Name:           oiwfs-prm
Version:        2.5
Release:        1%{?dist}
Summary:        Pixel router (prm) software loaded by the GMOS OIWFS crate
License:        Gemini Observatory (org-internal)
AutoReqProv:    no
# The payload is ppc604 objects the host only serves over NFS.
BuildArch:      noarch

%description
The prm V2-5.dev tree at %{prmdir}, copied verbatim from the production file
server: the ppc604 objects prmLib, prmControl and prmtest, the oiwfsPrm
databases the OIWFS startup loads, and the pixel-router switching scripts and
screens.

%install
mkdir -p %{buildroot}%{prmdir}
cp -a %{trees}%{prmdir}/. %{buildroot}%{prmdir}/
# Fail the build rather than ship a package the crate cannot boot from: these
# five are named literally by the OIWFS startup script.
for f in bin/ppc604/prmLib bin/ppc604/prmControl bin/ppc604/prmtest \
         data/oiwfsPrmTop.db data/oiwfsPrmSadTop.db; do
    [ -f "%{buildroot}%{prmdir}/$f" ] || { echo "ERROR: missing $f" >&2; exit 1; }
done

%files
%defattr(-,root,root,-)
%{prmdir}

%changelog
* Tue Oct 13 2026 Hawi Stecher <hawi.stecher@noirlab.edu> - 2.5-1
- Initial packaging: the deployed prm V2-5.dev tree, verbatim.
