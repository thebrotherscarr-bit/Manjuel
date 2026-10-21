## MCP Call

- **Action Keyword:** mcp_call
- **Description:** Calls one tool on a LOCAL MCP server this ground declares. Say it as "<server> <tool>", with any arguments as a JSON object after them — `atlas muster`, or `atlas flow_list {"project": "atlas"}`. A server is a dial, `MANJUEL_MCP_<NAME>` in .env, and its address must be loopback; anything else is refused by name, because the estate is local. Naming no tool, or one the server does not carry, answers with what that server does carry, so nothing needs a second skill to find its way. A call waits as long as a skill may run (MANJUEL_SKILL_TIMEOUT, 300 s, less five), so a suite the door runs can answer; a server that stalls past that is refused with the bound named. Use for "call <tool> on <server>", "what does <server> carry", "which MCP servers do we have".
- **Parameters Needed:** <content>The server and the tool, then any arguments as a JSON object — e.g. `atlas muster` or `atlas flow_list {"project": "atlas"}`. Blank falls back to the objective itself, which is read the same way.</content>
- **Says:** mcp call, call mcp, mcp tool, mcp servers, mcp server

A server can also be a PROGRAM spoken to over stdio: `MANJUEL_MCP_<NAME>_CMD=<command line>` in .env (manjuel/mcp_stdio.py). It is started only when its program, or the script node/python runs, is inside the ground; anything else is refused by name and nothing starts. It gets a minimal environment (never .env's keys), one process per call, started, asked and closed, under the same bound. `<name> tools` lists what it carries. A loopback dial of the same name wins. REA is declared with this line in .env:

    MANJUEL_MCP_REA_CMD=node worlds/harnesses/rea/node_modules/rea-agents/scripts/rea.mjs mcp
