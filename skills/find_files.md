# Skill: Find Files

- **Action Keyword:** find_files
- **Description:** Finds WHICH files in the ground match a glob (`**/*.py`, or a bare name at any depth), newest first with size and time. Read-only; never names a secret, client material, worlds/, a vault/ or .git/.
- **Parameters Needed:** <filepath>The glob or bare name, relative to the ground, e.g. **/*.py, skills/*.md or intent.py</filepath>
- **Path Args:** filepath -> ground
- **Says:** find files named, find the files, find files matching, glob for, which files match, recently changed files, the newest files

A folder's name alone lists every file under it. A glob with no `/` in it matches at any depth, the way .gitignore reads one; `**/` is any number of folders, `*` and `?` stay inside one, `[abc]` is a class and `{py,md}` a choice. The same folders `ground_grep` skips are skipped here.
