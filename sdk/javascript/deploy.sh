#!/bin/bash
#-------------------------------------------------------------------------------
# Zimagi JavaScript SDK deployment script
#-------------------------------------------------------------------------------
set -e

# Set working directory to script location
SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR"

# Check for required environment variables
if [ -z "$PKG_NPM_TOKEN" ]; then
    echo "Error: PKG_NPM_TOKEN environment variable must be defined to deploy the package"
    exit 1
fi

echo "Creating .npmrc configuration"
cat > ~/.npmrc <<EOF
//registry.npmjs.org/:_authToken=$PKG_NPM_TOKEN
EOF
chmod 600 ~/.npmrc

echo "Setting Zimagi package version"
jq --arg version "$(cat ../../app/VERSION | tr -d '\n\r')" '.version = $version' package.json > package.json.tmp
mv package.json.tmp package.json

echo "Installing dependencies"
npm install

echo "Building distribution files"
npm run build

echo "Publishing to npm registry"
npm publish --access public

echo "Cleaning up"
rm -f ~/.npmrc

echo "Deployment completed successfully"
