echo "Starting history wipe..."
cd /Users/antoineperrot/PycharmProjects/Enseignement/ipsa_msc_spacedata_students
# 1. Create a clean, history-less branch
git checkout --orphan temp_branch

# 2. Add files and create a clean commit
git add -A
git commit -m "Initial commit"

# 3. Replace the old main branch
git branch -D main
git branch -m main

# 4. Overwrite remote history on GitHub
git push -f origin main

echo "History wiped and pushed successfully!"
# Keeps the window open so you can see the confirmation or any errors
read -p "Press Enter to close this window..."
