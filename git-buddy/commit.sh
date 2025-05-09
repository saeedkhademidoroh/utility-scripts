#!/bin/bash

echo "🔧 Reword Commit Utility (Non-Interactive)"

# --- Hardcoded Inputs ---
COMMIT_HASH="46ebe6b35cd36f8e70c11d30fe60c0e35f50daf4"
NEW_TITLE="reword-commit.sh"
NEW_BODY="reword-commit.sh successfully executed"
OVERWRITE_MAIN=false  # Set to true to overwrite 'main'

# --- Verify commit exists ---
if ! git cat-file -e "$COMMIT_HASH"^{commit} 2>/dev/null; then
  echo "❌ Commit not found: $COMMIT_HASH"
  exit 1
fi

# --- Set target branch ---
if [ "$OVERWRITE_MAIN" = true ]; then
  TARGET_BRANCH="main"
else
  TARGET_BRANCH="reword-test"
  git checkout -B "$TARGET_BRANCH"
fi

# --- Extract metadata ---
AUTHOR_NAME=$(git show -s --format='%an' $COMMIT_HASH)
AUTHOR_EMAIL=$(git show -s --format='%ae' $COMMIT_HASH)
AUTHOR_DATE=$(git show -s --format='%aD' $COMMIT_HASH)
COMMITTER_DATE=$(git show -s --format='%cD' $COMMIT_HASH)

# --- Find base commit ---
BASE_HASH=$(git rev-list --parents -n 1 $COMMIT_HASH | cut -d' ' -f2)

# --- Rebase with auto-edit ---
GIT_SEQUENCE_EDITOR="sed -i 's/^pick $COMMIT_HASH/edit $COMMIT_HASH/'" \
git rebase -i $BASE_HASH || {
  echo "❌ Rebase failed. Aborting..."
  git rebase --abort
  exit 1
}

# --- Amend the commit with preserved metadata ---
GIT_AUTHOR_NAME="$AUTHOR_NAME" \
GIT_AUTHOR_EMAIL="$AUTHOR_EMAIL" \
GIT_AUTHOR_DATE="$AUTHOR_DATE" \
GIT_COMMITTER_DATE="$COMMITTER_DATE" \
git commit --amend -m "$NEW_TITLE"$'\n\n'"$NEW_BODY"

# --- Finish rebase ---
git rebase --continue || {
  echo "❌ Could not continue rebase. Aborting..."
  git rebase --abort
  exit 1
}

# --- Auto-push ---
git push origin "$TARGET_BRANCH" --force
echo "✅ Pushed to '$TARGET_BRANCH'"
