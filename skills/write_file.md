# Skill: Write Workspace File
- **Action Keyword:** write_file
- **Description:** Writes text, scripts, or markdown data to a file inside the workspace. A `.py` is checked before it is written and refused if it will not parse, imports the network, calls eval/exec/__import__, reaches importlib, or passes shell=True — the same check the coder's own landing makes. Nothing is written when it refuses. Prose is not judged.
- **Parameters Needed:** <filepath>filename.ext</filepath>, <content>text data</content>
- **Path Args:** filepath -> workspace
