#!/bin/zsh

echo "📂 Generating folder tree for the_undercover_victim_clean..."

# Ensure tree is installed
if ! command -v tree &> /dev/null
then
  echo "⚡ Installing tree via Homebrew..."
  brew install tree
fi

# Navigate to project folder
cd ~/Documents/the_undercover_victim_clean || exit 1

# Generate directory tree and save to Desktop
tree -d > ~/Desktop/clean_repo_tree.txt

echo "✅ Folder tree saved to ~/Desktop/clean_repo_tree.txt"
