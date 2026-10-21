# Skill: Run a Shell Command

- **Action Keyword:** run_shell
- **Description:** Runs one line of Git Bash in the ground, with its exit code and output. A short read list (git log, ls, cat, head, wc) runs at once; anything else only in Steward's driver, on the operator's card. Secrets, the network and git status are refused.
- **Parameters Needed:** <content>The command line to run, e.g. git log --oneline -5</content>
- **Says:** run the command, in the shell, run this in bash, run in bash, shell command

The gate is `manjuel/tools_shell.py`'s `classify()`, which mirrors the door's own shell gate (atlas/line/internal/tools/shellgate.go) and is stricter where an agent's hand must be: `git status` and a bare `git diff` are refused here because from a hand's shell they leave `.git/index.lock` in this ground, and the network, a remote, an install and the machine's own settings are refused rather than asked about (RULE 4, RULE 12). What the gate cannot read is a "write" and waits for the operator. The run stands in the ground with stdin closed, an environment holding no keys, a bound of 120 s, and its output cut to 8,000 characters (head and tail) with any key's value withheld.
