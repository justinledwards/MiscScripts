#!/bin/bash

# Check if the project folder is provided
if [ -z "$1" ]
then
  echo "Usage: $0 <path-to-node-project>"
  exit 1
fi

# Get the project folder and temp folder paths
PROJECT_FOLDER=$(realpath "$1")
TEMP_FOLDER=$(mktemp -d)

# Store the current working directory
CWD=$(pwd)

# Copy the project folder to the temp folder excluding node_modules and .git directories
rsync -av --exclude='node_modules' --exclude='.git' "$PROJECT_FOLDER/" "$TEMP_FOLDER/"

# Create a timestamped zip file with the original project folder's name
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
ZIP_NAME="$(basename "$PROJECT_FOLDER")_${TIMESTAMP}.zip"

# Change to the temp folder to avoid having the temp folder path in the zip file
cd "$TEMP_FOLDER" || exit

# Create the zip file with the directory structure, without including the temp folder itself
find . -type f -print | zip -r "$CWD/$ZIP_NAME" --names-stdin -q

# Change back to the original directory
cd - > /dev/null

# Remove the temp folder
rm -rf "$TEMP_FOLDER"

echo "Zipped project saved as $ZIP_NAME"
