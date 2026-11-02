#!/usr/bin/env bash
# Usage: ./commit_task.sh Q1   -> commits that task folder (one commit per task)
set -e
git add "$1"
git commit -m "Complete $1"
echo "Committed $1. Push with: git push"
