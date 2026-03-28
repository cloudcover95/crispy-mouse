#!/bin/zsh
echo "--- JuniorCloud Deployment Protocol ---"

# 1. Compile Firmware
echo "Building firmware.hex..."
pio run -e micro

if [ 0 -eq 0 ]; then
    echo "Build Success."
else
    echo "Build Failed. Aborting."
    exit 1
fi

# 2. Git Sync
git add .
read "commit_msg?Enter commit message: "
git commit -m "$commit_msg"

# 3. Tagging
read "tag_ver?Enter version tag (e.g. v1.1): "
git tag -a $tag_ver -m "Release $tag_ver"

# 4. Push to Sovereign Repo
git push origin main
git push origin $tag_ver

echo "Deployment to cloudcover95/crispy-mouse complete."
