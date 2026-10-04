Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$packageRoot = Join-Path $repoRoot "dist\plugins\blend-kit"
$sourceManifestPath = Join-Path $repoRoot "plugin.json"
$packageManifestPath = Join-Path $packageRoot "plugin.json"
$marketplacePath = Join-Path $repoRoot ".agents\plugins\marketplace.json"
$claudeManifestPath = Join-Path $packageRoot ".claude-plugin\plugin.json"
$claudeMarketplacePath = Join-Path $repoRoot ".claude-plugin\marketplace.json"
$cursorMarketplacePath = Join-Path $repoRoot ".cursor-plugin\marketplace.json"
$expectedSkills = @(
    "blend-generate-task",
    "blend-generate-test-spec",
    "blend-plan-implementation",
    "blend-review-artifacts",
    "blend-review-code"
)

foreach ($path in @($sourceManifestPath, $packageManifestPath, $marketplacePath, $claudeManifestPath, $claudeMarketplacePath, $cursorMarketplacePath)) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "Missing plugin package file: $path"
    }
}

$sourceManifest = Get-Content -LiteralPath $sourceManifestPath -Raw | ConvertFrom-Json
$packageManifest = Get-Content -LiteralPath $packageManifestPath -Raw | ConvertFrom-Json
$marketplace = Get-Content -LiteralPath $marketplacePath -Raw | ConvertFrom-Json
$claudeManifest = Get-Content -LiteralPath $claudeManifestPath -Raw | ConvertFrom-Json
$claudeMarketplace = Get-Content -LiteralPath $claudeMarketplacePath -Raw | ConvertFrom-Json
$cursorMarketplace = Get-Content -LiteralPath $cursorMarketplacePath -Raw | ConvertFrom-Json

if ([string]$sourceManifest.name -ne "blend-kit" -or [string]$packageManifest.name -ne "blend-kit") {
    throw "Source and packaged manifests must use the blend-kit plugin name."
}
if ([string]$sourceManifest.version -ne [string]$packageManifest.version) {
    throw "Source and packaged manifest versions differ."
}
if ([string]$claudeManifest.name -ne "blend-kit" -or [string]$claudeManifest.version -ne [string]$sourceManifest.version) {
    throw "Claude plugin manifest identity/version differs from plugin.json."
}
if ((Get-FileHash -LiteralPath $sourceManifestPath -Algorithm SHA256).Hash -ne
    (Get-FileHash -LiteralPath $packageManifestPath -Algorithm SHA256).Hash) {
    throw "Source and packaged plugin.json bytes differ."
}
if ([string]$marketplace.name -ne "tryhand-blend-kit") {
    throw "Unexpected marketplace name."
}
$entry = @($marketplace.plugins | Where-Object { [string]$_.name -eq "blend-kit" })
if ($entry.Count -ne 1) {
    throw "Marketplace must expose exactly one blend-kit entry."
}
if ([string]$entry[0].source.source -ne "local" -or
    [string]$entry[0].source.path -ne "./dist/plugins/blend-kit" -or
    [string]$entry[0].policy.installation -ne "AVAILABLE" -or
    [string]$entry[0].policy.authentication -ne "ON_INSTALL") {
    throw "Marketplace entry does not match the supported private distribution contract."
}

foreach ($catalog in @($claudeMarketplace, $cursorMarketplace)) {
    if ([string]$catalog.name -ne "tryhand-blend-kit") {
        throw "Unexpected Claude/Cursor marketplace name."
    }
    $catalogEntry = @($catalog.plugins | Where-Object { [string]$_.name -eq "blend-kit" })
    if ($catalogEntry.Count -ne 1 -or [string]$catalogEntry[0].source -ne "./dist/plugins/blend-kit") {
        throw "Claude/Cursor marketplace does not resolve the generated blend-kit package."
    }
    if ([string]$catalogEntry[0].version -ne [string]$sourceManifest.version) {
        throw "Claude/Cursor marketplace version differs from plugin.json."
    }
}

$skillRoot = Join-Path $packageRoot "skills"
$actualSkills = @(Get-ChildItem -LiteralPath $skillRoot -Directory -Force | Sort-Object Name | Select-Object -ExpandProperty Name)
if (($actualSkills -join "`n") -ne (($expectedSkills | Sort-Object) -join "`n")) {
    throw "Packaged skill inventory differs from the expected five skills."
}
foreach ($name in $expectedSkills) {
    if (-not (Test-Path -LiteralPath (Join-Path $skillRoot "$name\SKILL.md") -PathType Leaf)) {
        throw "Packaged skill is missing SKILL.md: $name"
    }
}

$forbidden = @(Get-ChildItem -LiteralPath $packageRoot -Recurse -Force | Where-Object {
    $_.Name -eq ".git" -or $_.Name -eq "__pycache__" -or $_.Name -like "~$*"
})
if ($forbidden.Count) {
    throw "Generated plugin contains forbidden runtime files."
}

$files = @(Get-ChildItem -LiteralPath $packageRoot -Recurse -File -Force | Sort-Object FullName)
$digestInput = foreach ($file in $files) {
    $relative = [IO.Path]::GetRelativePath($packageRoot, $file.FullName).Replace("\", "/")
    "$relative`0$((Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant())`n"
}
$digestBytes = [Text.Encoding]::UTF8.GetBytes(($digestInput -join ""))
$sha = [Security.Cryptography.SHA256]::Create()
try {
    $digest = [Convert]::ToHexString($sha.ComputeHash($digestBytes)).ToLowerInvariant()
}
finally {
    $sha.Dispose()
}

Write-Output (@{
    plugin = "blend-kit@tryhand-blend-kit"
    version = [string]$sourceManifest.version
    skills = $actualSkills.Count
    files = $files.Count
    digest = $digest
} | ConvertTo-Json -Compress)
