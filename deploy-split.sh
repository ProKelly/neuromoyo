#!/usr/bin/env bash
# ============================================================
# YouthParent+ | split main into two deploy-only branches
# ============================================================
# Run this from the repo root, on main, after committing your
# changes normally. It rewrites two branches so that:
#
#   frontend-deploy  →  contents of /frontend, at branch root
#   backend-deploy   →  contents of /backend,  at branch root
#
# Vercel watches frontend-deploy. Heroku watches backend-deploy.
# Nothing on main (docs, database/, the other app) ever reaches
# either platform.
#
# Safe to re-run any time — it force-pushes fresh split branches
# from whatever is currently committed on main.
# ============================================================
set -euo pipefail

if [[ $(git branch --show-current) != "main" ]]; then
  echo "Switch to main first: git checkout main"
  exit 1
fi

if ! git diff-index --quiet HEAD --; then
  echo "You have uncommitted changes. Commit or stash them first."
  exit 1
fi

echo "==> Splitting frontend/ ..."
git branch -D frontend-deploy-tmp 2>/dev/null || true
git subtree split --prefix=frontend -b frontend-deploy-tmp
git push origin frontend-deploy-tmp:frontend-deploy --force
git branch -D frontend-deploy-tmp

echo "==> Splitting backend/ ..."
git branch -D backend-deploy-tmp 2>/dev/null || true
git subtree split --prefix=backend -b backend-deploy-tmp
git push origin backend-deploy-tmp:backend-deploy --force
git branch -D backend-deploy-tmp

echo "==> Done."
echo "    frontend-deploy pushed  → Vercel will redeploy automatically"
echo "    backend-deploy pushed   → Heroku will redeploy automatically"
