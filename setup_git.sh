# Git Setup and Push Script

# Install Git LFS (if not already installed)
# Download from: https://git-lfs.github.com/
# Or use: winget install -e --id GitHub.GitLFS

# Initialize Git LFS
git lfs install

# Initialize Git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Coral Bleaching Detection with ResNet50 model"

# Rename branch to main
git branch -M main

# Add your remote repository (replace with your actual GitHub repo URL)
# git remote add origin https://github.com/yourusername/coral-bleaching-detection.git

# Push to GitHub (uncomment after adding remote)
# git push -u origin main

# Note: The .pth model file will be tracked with Git LFS automatically
