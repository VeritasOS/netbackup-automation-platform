#!/bin/bash

# $Copyright: Copyright (c) 2024 Veritas Technologies LLC. All rights reserved $

help()
{
    echo ""
    echo "Usage: $0 [-h|-r|-v|-d|-t]"
    echo -e "-h      Prints this help."
    echo -e "-r      Provide release string in major.minor.patch.build format. For e.g. 10.1.1.0"
    echo -e "-v      Provide EEB version. E.g. 1"
    echo -e "-d      Provide Etrack incident number. This is the defect fixed in this EEB."
    echo -e "-t      Provide location to save the RPM package."
    exit 1
}

while getopts "h:v:r:d:t:" opt
do
  case "$opt" in
    h ) HELP=1 ;;
    v ) VERSION="$OPTARG" ;;
    r ) RELEASE="$OPTARG" ;;
    d ) ETRACK="$OPTARG" ;;
    t ) TARGETD="$OPTARG" ;;
    ? ) help ;;
  esac
done
NAME="VRTSnbeeb"

if [ -n "$HELP" ]; then
    help
fi
if [ -z "$VERSION" ] || [ -z "$RELEASE" ] || [ -z "$ETRACK" ] || [ -z "$TARGETD" ]
then
    echo "You have either not provided any option or provided incorrect option."
    help
fi

BUILD=1
TARGET="-bb"
VENDOR="Veritas Technologies LLC"
PROVIDES="Provides: ${NAME} includes fixes for defect id: ${ETRACK}"

# Generate Spec file
SPECFILE=$(mktemp)
cat <<EOF > ${SPECFILE}
#----------- spec file ---------------
Name:                   VRTSnbeeb_${ETRACK}
Release:                ${RELEASE}
Version:                ${VERSION}
Vendor:                 ${VENDOR}
#Group:                  ${GROUP}
Summary:                EEB for NetBackup ${RELEASE} %{name}
License:                Copyright %{vendor}
${PROVIDES}
%Description
Includes fix for defect:${ETRACK}
This is a fake rpm for EEB ${NAME} ${RELEASE} so no actual files registered. For the RPM details check /usr/openv/pack/pack.summary
%files
EOF

# Build it 

if [ -n "$BUILD" ]; then
    BUILD_LOG=$(mktemp)
    rpmbuild --define '_rpmdir $(mktemp)' ${TARGET} "${SPECFILE}" > "${BUILD_LOG}"
    if [ $? != 0 ]
    then
      echo "ERROR: Could not build rpm for ${NAME}!"
    fi
    PKG=$(awk '/^Wrote:/ { print $2 }' < "${BUILD_LOG}" )
    rm "${BUILD_LOG}"
    rm "${SPECFILE}"

    echo "DONE!  created ${PKG}..."
    mv $PKG $TARGETD
fi
