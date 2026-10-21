# Skill: Grep the Ground

- **Action Keyword:** ground_grep
- **Description:** Finds WHERE a regex is in the ground's text files: `path:line: text`, at most 200 hits. Lower case matches any case. Read-only; never opens a secret, client material, worlds/, a vault/ or .git/.
- **Parameters Needed:** <content>The pattern, a Python regex, e.g. `def _ground_read` or `never_written\(`</content> <filepath>Optional: a folder (`manjuel`), a file, or a glob (`**/*.py`, `skills/*.md`) to search within; leave it out for the whole ground</filepath>
- **Path Args:** filepath -> ground
- **Says:** grep for, grep the ground, grep the code, search the code for, search the source for, which files mention, find every use of

A pattern carrying a capital letter matches case as written (smart case). A bad regex is refused with the regex's own error and nothing is searched. A glob with no `/` in it matches at any depth (`*.py`, `skills.py`). Each line of text is cut to 200 characters; past 200 hits the reply says how many more were not shown.
