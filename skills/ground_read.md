## Ground Read

- **Action Keyword:** ground_read
- **Description:** Reads one file from the ground (the Research folder) as it is on disk right now — pipelines.md, memory.md, a seat's own file, source in manjuel/. Read-only, refuses secrets, stays inside the ground. Use when a question needs the CURRENT contents of a real file, not the index's snapshot of it.
- **Parameters Needed:** <content>The file's path relative to the ground, e.g. pipelines.md or agents/steward.md</content>. A LARGE file comes back as part 1 of N with its section headings listed; to move the window, send the path as <filepath> and the part as <content> — either a number (`2`) or a heading's text (`Fix log`). A large .py comes back as THE MAP instead: its definitions and its module-level names with their line ranges, and any one of them is fetched whole by name (`_NEVER_WRITTEN_TOP`, `SkillLibrary.execute`). Two tags means file plus part; one tag always means the whole file.
- **Path Args:** content -> ground, filepath -> ground
