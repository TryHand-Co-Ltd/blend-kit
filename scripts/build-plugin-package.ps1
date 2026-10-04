param(
    [string]$Python = "python"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$packageRoot = [IO.Path]::GetFullPath((Join-Path $repoRoot "dist\plugins\blend-kit"))
$stagingRoot = [IO.Path]::GetFullPath((Join-Path $repoRoot "dist\.blend-kit-plugin-staging"))
$repoPrefix = $repoRoot.TrimEnd([char[]]"\/") + [IO.Path]::DirectorySeparatorChar

foreach ($path in @($packageRoot, $stagingRoot)) {
    if (-not $path.StartsWith($repoPrefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Plugin build path escapes the repository: $path"
    }
}
if ([IO.Path]::GetRelativePath($repoRoot, $packageRoot) -ne "dist\plugins\blend-kit" -or
    [IO.Path]::GetRelativePath($repoRoot, $stagingRoot) -ne "dist\.blend-kit-plugin-staging") {
    throw "Unexpected plugin build targets."
}

$manifestPath = Join-Path $repoRoot "plugin.json"
if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) {
    throw "Missing canonical plugin manifest: $manifestPath"
}
$manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
if ([string]$manifest.name -ne "blend-kit" -or [string]::IsNullOrWhiteSpace([string]$manifest.version)) {
    throw "plugin.json must declare blend-kit and a non-empty version."
}

foreach ($path in @($stagingRoot, $packageRoot)) {
    if (Test-Path -LiteralPath $path) {
        Remove-Item -LiteralPath $path -Recurse -Force
    }
}

try {
    & $Python (Join-Path $repoRoot "scripts\build-kit.py") --source $repoRoot --output $stagingRoot --profiles codex --check
    if ($LASTEXITCODE -ne 0) {
        throw "BLEND Kit source package build failed."
    }

    $generatedSkills = Join-Path $stagingRoot "codex\.agents\skills"
    if (-not (Test-Path -LiteralPath $generatedSkills -PathType Container)) {
        throw "Generated Codex skill root is missing: $generatedSkills"
    }

    New-Item -ItemType Directory -Path (Join-Path $packageRoot "skills") -Force | Out-Null
    Copy-Item -LiteralPath $manifestPath -Destination (Join-Path $packageRoot "plugin.json")
    New-Item -ItemType Directory -Path (Join-Path $packageRoot ".claude-plugin") -Force | Out-Null
    Copy-Item -LiteralPath (Join-Path $repoRoot ".claude-plugin\plugin.json") -Destination (Join-Path $packageRoot ".claude-plugin\plugin.json")
    foreach ($skill in Get-ChildItem -LiteralPath $generatedSkills -Directory -Force) {
        Copy-Item -LiteralPath $skill.FullName -Destination (Join-Path $packageRoot "skills") -Recurse
    }

    $readme = @'
# BLEND Kit Plugin Package

Generated private-marketplace package. Do not edit files under this directory directly.

- Canonical manifest: repository root `plugin.json`
- Canonical skills: repository root `skills/` plus the shared resources resolved by `scripts/build-kit.py`
- Rebuild: `pwsh -File scripts/build-plugin-package.ps1`
'@
    [IO.File]::WriteAllText((Join-Path $packageRoot "README.md"), $readme, [Text.UTF8Encoding]::new($false))
}
finally {
    if (Test-Path -LiteralPath $stagingRoot) {
        Remove-Item -LiteralPath $stagingRoot -Recurse -Force
    }
}

& (Join-Path $repoRoot "scripts\check-plugin-package.ps1")
if ($LASTEXITCODE -ne 0) {
    throw "Generated plugin package validation failed."
}

Write-Output "Built BLEND Kit plugin $($manifest.version) at dist/plugins/blend-kit."
