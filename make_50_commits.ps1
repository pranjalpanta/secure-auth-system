# make_50_commits_backdated.ps1
param(
  [int]$Commits = 50,
  [string]$Branch = "main"
)

$ErrorActionPreference = "Stop"

function Fail($msg) { Write-Host "[ERROR] $msg" -ForegroundColor Red; exit 1 }

# 1. Date Configuration
$startDate = Get-Date -Year 2026 -Month 2 -Day 10 -Hour 09 -Minute 0 -Second 0
$endDate   = Get-Date -Year 2026 -Month 3 -Day 1 -Hour 17 -Minute 0 -Second 0
$totalDuration = $endDate - $startDate
# Calculate interval so 50 commits fit perfectly in the time range
$secondsBetweenCommits = $totalDuration.TotalSeconds / $Commits

# 2. Git Safety Checks
git rev-parse --is-inside-work-tree *> $null
if ($LASTEXITCODE -ne 0) { git init } # Initialize if not a repo

git checkout $Branch *> $null
if ($LASTEXITCODE -ne 0) { git checkout -B $Branch *> $null }

git diff --cached --quiet
if ($LASTEXITCODE -ne 0) { Fail "You already have staged changes. Run: git reset" }

# 3. Gather Files
$tracked = (git ls-files) -split "`n" | Where-Object { $_ -and $_.Trim() -ne "" }
$untracked = (git ls-files -o --exclude-standard) -split "`n" | Where-Object { $_ -and $_.Trim() -ne "" }
$all = ($untracked + $tracked) | Select-Object -Unique

if ($all.Count -eq 0) { Fail "No files available to commit." }

$chunkSize = [Math]::Ceiling($all.Count / $Commits)

# 4. Make Backdated Commits
$idx = 0
for ($i=1; $i -le $Commits; $i++) {
    if ($idx -ge $all.Count) { break }

    $end = [Math]::Min($idx + $chunkSize - 1, $all.Count - 1)
    $chunk = $all[$idx..$end]

    foreach ($path in $chunk) {
        if ($path -and (Test-Path $path)) { git add -- "$path" *> $null }
    }

    git diff --cached --quiet
    if ($LASTEXITCODE -eq 0) { $idx = $end + 1; continue }

    # --- THE DATE MANIPULATION MAGIC ---
    $currentCommitDate = $startDate.AddSeconds($secondsBetweenCommits * ($i - 1))
    $gitDateString = $currentCommitDate.ToString("yyyy-MM-ddTHH:mm:ss")
    
    $env:GIT_AUTHOR_DATE = $gitDateString
    $env:GIT_COMMITTER_DATE = $gitDateString
    # -----------------------------------

    $msg = ("Phase {0:D2}/{1:D2}: Adding project modules" -f $i, $Commits)
    git commit -m "$msg" *> $null
    Write-Host "[OK] $gitDateString -> $msg" -ForegroundColor Green

    $idx = $end + 1
}

# Cleanup environment variables
Remove-Item Env:GIT_AUTHOR_DATE
Remove-Item Env:GIT_COMMITTER_DATE

Write-Host "`n[DONE] Timeline generated from Feb 10 to Mar 1." -ForegroundColor Cyan
Write-Host "Verify with: git log --format=fuller"