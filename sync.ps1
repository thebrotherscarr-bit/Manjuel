#!/usr/bin/env pwsh
# sync.ps1 -- bring this PC level with GitHub: Manjuel, Atlas and SecondBrain's code.
#
# His word, 2026-10-22: "my shit on my pc isnt staying updated with all the changes
# now ... make sure that all the github stuff is staying aligned within the system",
# and: "NOPE not fucking hidden task scheduler. I WANT TO BE ABLE TO CONTROL MY SHIT!"
# So nothing here runs by itself. Atlas's Update button and SecondBrain's Sync button
# run it, and only when he presses them.
#
#   sync.ps1 -Check    what each repository is behind, what is coming, what stops it (JSON)
#   sync.ps1           bring each one level, fast-forward only, and say every step
#
# Each repository moves only on its own line (Manjuel and Atlas: main; SecondBrain:
# the branch its checkout follows), only with no unsaved work, and never while a
# sitting is open (an engine would be running old code under him). When Atlas moved,
# atlas/update.ps1 rebuilds and restarts the door and the glass. When the notes kernel
# moved, the relay and the notes server are restarted on it.
# Pure ASCII, so PowerShell 5.1 reads it whatever the code page.

param([switch]$Check)

$ErrorActionPreference = 'Stop'
$ground = $PSScriptRoot
$env:GIT_TERMINAL_PROMPT = '0'
$Log = Join-Path $ground 'sync.log'

$repos = @(
    @{ Name = 'Manjuel';     Dir = $ground;                                   Line = 'main' },
    @{ Name = 'Atlas';       Dir = (Join-Path $ground 'atlas');               Line = 'main' },
    @{ Name = 'SecondBrain'; Dir = (Join-Path $ground 'worlds\jesster');      Line = '' }
)

function Say([string]$t) {
    $line = "{0}  {1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $t
    if (-not $Check) { Add-Content -Path $Log -Value $line }
    Write-Output $t
}

function G([string]$dir, [string[]]$a) {
    $out = & git.exe -C $dir @a 2>&1
    return @{ Ok = ($LASTEXITCODE -eq 0); Out = (($out | Out-String).Trim()) }
}

function SittingOpen {
    $f = Join-Path $ground 'sessions\sessions.jsonl'
    if (-not (Test-Path $f)) { return $null }
    $last = Get-Content $f -Tail 1
    if (-not $last) { return $null }
    $row = $last | ConvertFrom-Json
    if ($row.ended) { return $null }
    return $row.n
}

# What one repository is, against GitHub: fetched first.
function State($r) {
    $s = [ordered]@{ name = $r.Name; dir = $r.Dir; branch = ''; line = ''; behind = 0; ahead = 0; dirty = $false; changes = @(); why_not = '' }
    if (-not (Test-Path (Join-Path $r.Dir '.git'))) { $s.why_not = 'not a repository here'; return $s }
    $s.branch = (G $r.Dir @('rev-parse', '--abbrev-ref', 'HEAD')).Out
    $line = $r.Line
    if (-not $line) {
        $u = G $r.Dir @('rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{u}')
        if (-not $u.Ok) { $s.why_not = "the branch '$($s.branch)' follows nothing on GitHub"; return $s }
        $line = $u.Out -replace '^origin/', ''
    }
    $s.line = $line
    $f = G $r.Dir @('fetch', '-q', 'origin', $line)
    if (-not $f.Ok) { $s.why_not = "GitHub could not be asked: $($f.Out)"; return $s }
    $s.behind = [int](G $r.Dir @('rev-list', '--count', "HEAD..origin/$line")).Out
    $s.ahead = [int](G $r.Dir @('rev-list', '--count', "origin/$line..HEAD")).Out
    if ($s.behind -gt 0) {
        $s.changes = @((G $r.Dir @('log', '--format=%s', '-n', '8', "HEAD..origin/$line")).Out -split "`n" | Where-Object { $_ })
    }
    & git.exe -C $r.Dir diff-index --quiet HEAD -- 2>$null
    $s.dirty = ($LASTEXITCODE -ne 0)
    if ($r.Name -eq 'Atlas') {
        # the running glass may be older than the checkout even when the checkout is level
        $exe = Join-Path $r.Dir 'webapp\atlas-webapp.exe'
        $built = (& go version -m $exe 2>$null | Select-String 'vcs.revision=([0-9a-f]+)').Matches.Groups[1].Value
        $tip = (G $r.Dir @('rev-parse', "origin/$line")).Out
        $s.rebuild = [bool]($built -and $tip -and $built -ne $tip)
        if ($s.rebuild -and $s.behind -eq 0) { $s.changes = @('the running door and glass are older than main: rebuild them') }
    }
    if ($s.branch -ne $line) { $s.why_not = "it is on '$($s.branch)', not $line" }
    elseif ($s.dirty) { $s.why_not = 'it has unsaved work' }
    elseif ($s.ahead -gt 0 -and $s.behind -gt 0) { $s.why_not = "it has $($s.ahead) commit(s) GitHub does not, so it cannot move forward alone" }
    return $s
}

function Restart([string]$match, [string[]]$argv, [string]$what) {
    $p = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match $match } | Select-Object -First 1
    if (-not $p) { return }
    Stop-Process -Id $p.ProcessId -Force
    Start-Sleep -Milliseconds 800
    Start-Process -FilePath python -ArgumentList $argv -WorkingDirectory (Join-Path $ground 'worlds\jesster') -WindowStyle Hidden
    Say "  restarted the $what on the new notes kernel"
}

$states = @($repos | ForEach-Object { State $_ })
$sitting = SittingOpen

if ($Check) {
    $total = 0
    foreach ($s in $states) { $total += [int]$s.behind; if ($s.rebuild -and -not $s.behind) { $total += 1 } }
    [ordered]@{ repos = $states; sitting_open = $sitting; behind = $total } |
        ConvertTo-Json -Depth 4 -Compress
    exit 0
}

Say 'sync: bringing this PC level with GitHub'
if ($sitting) {
    Say "sync: sitting $sitting is open -- close it first; nothing was moved"
    exit 1
}
$i = 0
foreach ($s in $states) {
    $r = $repos[$i]; $i++
    if ($s.why_not) { Say "$($s.name): left as it is -- $($s.why_not)"; continue }
    if ($s.behind -eq 0 -and -not $s.rebuild) { Say "$($s.name): level with GitHub"; continue }
    if ($s.name -eq 'Atlas') {
        Say "Atlas: $($s.behind) new -- pulling, rebuilding the door and the glass, restarting them (atlas\update.ps1)"
        & (Join-Path $r.Dir 'update.ps1') | ForEach-Object { Say "  $_" }
        continue
    }
    $before = (G $r.Dir @('rev-parse', 'HEAD')).Out
    $m = G $r.Dir @('merge', '-q', '--ff-only', "origin/$($s.line)")
    if (-not $m.Ok) { Say "$($s.name): could not move forward -- $($m.Out)"; continue }
    Say "$($s.name): $($s.behind) new, now level -- $((G $r.Dir @('log', '--oneline', '-1')).Out)"
    if ($s.name -eq 'SecondBrain') {
        $kernel = (G $r.Dir @('diff', '--name-only', $before, 'HEAD', '--', 'notes')).Out
        if ($kernel) {
            $cli = Join-Path $r.Dir 'notes\cli.py'
            $vault = Join-Path $ground 'worlds\notes'
            Restart 'cli\.py.* bridge ' @($cli, '--vault', $vault, 'bridge', (Join-Path $ground 'worlds\secondbrain-relay')) 'relay'
            Restart 'cli\.py"? serve' @($cli, 'serve') 'notes server'
        }
        Say '  the SecondBrain app itself updates with its own Update button (its release build)'
    }
    if ($s.name -eq 'Manjuel') { Say '  Manjuel: an engine opened from now on runs the new code' }
}
Say 'sync: done'
