cd ~/projects/ml/src

for dir in */; do
  cd "$dir" || continue
  if [ -d ".git" ]; then
    echo "📁 $dir"
    git symbolic-ref --short HEAD
    git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || echo "⚠️  No upstream set"
    echo
  fi
  cd ..
done
