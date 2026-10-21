# Skill: Apply a Patch

- **Action Keyword:** apply_patch
- **Description:** Changes several files of the ground at once, on a LINE OF WORK, whole or not at all: every hunk is found first, and one miss writes nothing. ground_write's walls: never main, no new folder, terminators kept.
- **Parameters Needed:** <content>The patch: a line `*** Begin Patch`; then `*** Add File: path` (every line after it begins with +), `*** Update File: path` (optionally `*** Move to: path`) with `@@` hunks (context lines begin with a space, removed with -, added with +), or `*** Delete File: path`; then a line `*** End Patch`</content>
- **Says:** apply this patch, apply the patch, apply a patch, patch these files, a multi-file patch

Each hunk's old lines (its context and removed lines) must be found exactly once in the file as it stands, by whole lines: exactly, then with trailing spaces ignored, then with curly quotes, long dashes and odd spaces made plain. When they appear more than once, an `@@ line` naming the definition they are in picks the one after it. A patch with no `*** End Patch` is refused as possibly cut off; a ```fence or a shell heredoc around it is ignored. A delete is refused unless the file is tracked and unchanged since the last commit, so it can be undone from history. The reply begins `Patched` and gives one line per file; the work is unsaved until git_commit lands it on the line.
