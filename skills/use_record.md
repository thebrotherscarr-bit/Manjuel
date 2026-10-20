# Skill: Use Record

- **Action Keyword:** use_record
- **Says:** record a use
- **Description:** The engine's own after-tool hook: after every skill or tool call it appends one line to logs/uses.jsonl -- when, the tool, whether it answered or refused, how long it took, and who called -- and skill_report weighs each skill off those lines (its uses, its failures and how long it usually takes). It is never called by name: asked for, it refuses and writes nothing. It writes only for a library the engine loaded for a sitting, never for the strokes. His card of 2026-10-19 (WHAT'S LEFT H32): every use marked, catalogued and weighed.
- **Hooks:** after_tool
- **Parameters Needed:** None
