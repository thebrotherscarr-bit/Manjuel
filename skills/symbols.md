# Skill: Symbols

- **Action Keyword:** symbols
- **Description:** Where a name is DECLARED in this ground, read straight off the disk — file and line for every def, class, func, type or exported binding, in Python, Go and JavaScript, with the other files that name it. Given no name it returns the MAP of the ground instead: every code file that declares anything, ordered by how many other files lean on what it declares, with each one's top symbols. Deterministic and current: no model, no embedding, no cache, nothing that can be stale or invented. Use it BEFORE reading or searching — "where is X", "what defines Y", "what is this estate shaped like" — because semantic_search answers with passages ABOUT a subject and this answers with the line.
- **Says:** where is, what defines, where is it defined, map the ground, the shape of the ground, which file declares
- **Parameters Needed:** <content>One symbol name, e.g. tagSend or chunk_text. Leave it out for the map of the whole ground.</content>
