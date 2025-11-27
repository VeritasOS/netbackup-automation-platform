#!/bin/bash

# $Copyright: Copyright (c) 2025 Cohesity, Inc. All rights reserved $

# create_eeb_pkg_marker.sh
# Script to create a native Solaris PKG marker package for NetBackup EEB

help()
{
    echo ""
    echo "Usage: $0 [-h|-r|-v|-d|-t]"
    echo -e "-h      Prints this help."
    echo -e "-r      Provide release string in major.minor.patch.build format. For e.g. 10.1.1.0"
    echo -e "-v      Provide EEB version. E.g. 1"
    echo -e "-d      Provide Etrack incident number. This is the defect fixed in this EEB."
    echo -e "-t      Provide location to save the PKG package."
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



# Solaris PKG abbreviation must be <= 9 chars, alphanumeric, unique per EEB, and start with a letter
# Use EB<DEFECT> (truncated to 9 chars if needed)
PKG_ABBR="EB${ETRACK}"
# Remove non-alphanumeric and ensure <=9 chars
PKG_ABBR="$(echo "$PKG_ABBR" | tr -cd '[:alnum:]' | cut -c1-9)"
# Detect architecture: i386 or sun4v
ARCH=$(uname -p)
if [[ "$ARCH" == "i386" ]]; then
  PKG_ARCH="i386"
elif [[ "$ARCH" == "sparc" || "$ARCH" == "sun4v" ]]; then
  PKG_ARCH="sun4v"
else
  PKG_ARCH="all"
fi
FULL_PKG_NAME="VRTSnbeeb_${ETRACK}-${VERSION}-${RELEASE}.${PKG_ARCH}"
PKG_NAME="$FULL_PKG_NAME"
CURRENT_DIR="$(pwd)"
PKG_DIR="${CURRENT_DIR}/${PKG_NAME}"
rm -rf "$PKG_DIR"
mkdir -p "$PKG_DIR/reloc"
MARKER_FILE="$PKG_DIR/reloc/${FULL_PKG_NAME}.marker"
touch "$MARKER_FILE"
echo "NetBackup EEB marker package for $PKG_NAME version $VERSION" > "$MARKER_FILE"


# Create pkginfo
cat > "$PKG_DIR/pkginfo" <<EOF
PKG=${PKG_ABBR}
NAME=${PKG_NAME}
VERSION=${VERSION}
ARCH=${PKG_ARCH}
CATEGORY=application
VENDOR="Veritas Technologies LLC"
PSTAMP=$(date +%Y%m%d%H%M)
DESC="NetBackup EEB marker package for $PKG_NAME version $VERSION"
BASEDIR="/opt"
CLASSES="none"
EOF

# Create postinstall script
cat > "$PKG_DIR/postinstall" <<EOPI
#!/bin/sh
echo "Dummy package installed successfully."
exit 0
EOPI
chmod +x "$PKG_DIR/postinstall"


# Create prototype file
echo "i pkginfo=./pkginfo" > "$PKG_DIR/prototype"
echo "i postinstall=./postinstall" >> "$PKG_DIR/prototype"
echo "d none reloc 0755 root bin" >> "$PKG_DIR/prototype"
echo "f none reloc/${FULL_PKG_NAME}.marker 0644 root bin" >> "$PKG_DIR/prototype"


cd "$PKG_DIR"
pkgmk -o -r "$PKG_DIR"

# Translate to a real package file


cd /var/spool/pkg
PKGFILE="/tmp/${FULL_PKG_NAME}.pkg"
pkgtrans -s /var/spool/pkg "$PKGFILE" "$PKG_ABBR"

mkdir -p "$TARGETD"
mv "$PKGFILE" "$TARGETD/"

# Display the package path
echo "Package successfully created: ${TARGETD}/${FULL_PKG_NAME}.pkg"

# Delete the package build artifacts
rm -rf "$PKG_DIR"
rm -rf "/var/spool/pkg/${PKG_ABBR}"