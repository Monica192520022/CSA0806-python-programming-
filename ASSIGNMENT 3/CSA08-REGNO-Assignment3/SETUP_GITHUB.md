# One-time setup
1. Rename this folder to `CSA08-<YourRegisterNumber>-Assignment3`.
2. Open it in VS Code (File > Open Folder).
3. Create a venv: `python -m venv .venv` then activate it, then `pip install -r requirements.txt`.
4. Create an EMPTY repo on GitHub named exactly `CSA08-<RegisterNumber>-Assignment3`
   (public, or private and add the faculty as collaborator).
5. In the VS Code terminal:
```
git init
git branch -M main
git remote add origin https://github.com/<username>/CSA08-<RegisterNumber>-Assignment3.git
git add README.md requirements.txt .gitignore
git commit -m "Initial setup"
git push -u origin main
```
6. After finishing EACH task: `bash commit_task.sh Q1` (or use `git add Q1 && git commit -m "Q1 done"`), then `git push`.
   Commit history is checked – do NOT upload everything on the last day.
7. Paste the repo link on the assignment sheet and the report cover page.
