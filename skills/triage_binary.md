# Skill: Triage Binary

- **Action Keyword:** triage_binary
- **Description:** Reads a file's BYTES and reports only what they say: its format by magic bytes (ELF, PE and whether .NET, Mach-O incl. fat, WASM, ZIP, ASAR, gzip, PDF, PNG), entropy whole and per 4 KB window with the share above 7.2 (packed or encrypted-looking), ASCII and UTF-16LE strings sorted by kind, and the first 64 bytes. A secret-looking string is counted, never printed. Read-only; at most 64 MB.
- **Parameters Needed:** <filepath>The file, relative to the workspace (agent_workspace/) or the ground; the workspace is tried first</filepath>
- **Path Args:** filepath -> ground, content -> ground
- **Says:** triage this binary, triage the binary, triage the file, what kind of file is, entropy of, strings in the binary, is it packed

What it reads off the header, and nothing more: ELF class, byte order, type and machine; PE32 or PE32+, machine, DLL or EXE, subsystem, the header's section count, and .NET by its CLI header; Mach-O class, cpu and file type, and a fat header's architectures; the WASM version; a ZIP's entry count, with JAR, APK or Office hints taken from its entry names only; the PDF version; a PNG's size. No sections, imports or mitigations are inferred. Strings are 5 or more printable characters; the first 400 by offset are sorted into url, secret-looking, crypto, path, error and other, and a few of each are shown. A secret-looking string is counted and never printed (LAW 9: keys are silent), and the first 64 bytes are withheld when one begins inside them. A file over 64 MB is read to 64 MB and the reply says it was cut. The jail and the refusals are `inspect`'s: the workspace first, then the ground; never a secret, client material, worlds/ or a vault/.
