#!/usr/bin/env bash
# Build NexusChat .app and .pkg for macOS
# Usage: bash build_pkg.sh

# prerequisites: brew install python3 pkgbuild

set -e

# Clean previous builds
rm -rf build dist NexusChat-0.3.pkg

# Create the macOS .app bundle
echo "Building macOS app via py2app..."
python3 setup.py py2app

# Create a .pkg installer
APP_PATH="dist/NexusChat.app"
PKG_NAME="NexusChat-0.3.pkg"
echo "Creating .pkg installer..."
pkgbuild --install-location "/Applications" --component "$APP_PATH" "$PKG_NAME"
echo "Built package: $PKG_NAME"