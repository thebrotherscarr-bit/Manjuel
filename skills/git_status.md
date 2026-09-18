# Skill: Git Status
- **Action Keyword:** git_status
- **Description:** Reports the repository state - branch, current commit, whether the ground is clean or dirty, and whether remote operations are permitted. Read-only; it changes nothing. Use it before committing, or to answer questions about what version the work is at.
- **Parameters Needed:** <filepath>OPTIONAL. The world to act in -- a folder inside this ground that holds its own repository, e.g. atlas. Leave it out and this acts on the ground itself, which is what it has always done.</filepath>
- **Path Args:** filepath -> ground
