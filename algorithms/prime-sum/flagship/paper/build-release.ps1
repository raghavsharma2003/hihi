[CmdletBinding()]
param(
    [string]$OutputDirectory = "",
    [switch]$KeepBuildDirectory
)

$ErrorActionPreference = "Stop"

$paperDirectory = [System.IO.Path]::GetFullPath($PSScriptRoot)
$repositoryRoot = [System.IO.Path]::GetFullPath(
    (Join-Path $paperDirectory "..\..\..\..")
)
$mainSource = Join-Path $paperDirectory "main.tex"
$tectonic = Join-Path $repositoryRoot ".tools\tectonic\tectonic.exe"
$artifactName =
    "simultaneous-hard-edge-weighted-hyperelliptic-prime-races.pdf"

if (-not (Test-Path -LiteralPath $mainSource -PathType Leaf)) {
    throw "Missing main source: $mainSource"
}
if (-not (Test-Path -LiteralPath $tectonic -PathType Leaf)) {
    throw "Missing pinned Tectonic executable: $tectonic"
}

if ([string]::IsNullOrWhiteSpace($OutputDirectory)) {
    $OutputDirectory = Join-Path $repositoryRoot "output\pdf"
}
$OutputDirectory = [System.IO.Path]::GetFullPath($OutputDirectory)
New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null

$buildDirectory = Join-Path (
    [System.IO.Path]::GetTempPath()
) ("focused-hyperelliptic-build-" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $buildDirectory | Out-Null

try {
    $relativeMain = "algorithms/prime-sum/flagship/paper/main.tex"
    $resolvedRelativeMain = [System.IO.Path]::GetFullPath(
        (Join-Path $repositoryRoot $relativeMain)
    )
    if ($resolvedRelativeMain -ne $mainSource) {
        throw "The build script's repository layout assumption is false"
    }

    Push-Location $repositoryRoot
    try {
        $savedPreference = $ErrorActionPreference
        $ErrorActionPreference = "Continue"
        $buildOutput = & $tectonic --keep-logs --keep-intermediates `
            --outdir $buildDirectory $relativeMain 2>&1
        $exitCode = $LASTEXITCODE
        $ErrorActionPreference = $savedPreference
    }
    finally {
        Pop-Location
    }

    $buildOutput | ForEach-Object { Write-Host $_ }
    if ($exitCode -ne 0) {
        throw "Tectonic failed with exit code $exitCode"
    }

    $builtPdf = Join-Path $buildDirectory "main.pdf"
    $buildLog = Join-Path $buildDirectory "main.log"
    if (-not (Test-Path -LiteralPath $builtPdf -PathType Leaf)) {
        throw "Tectonic exited successfully but did not create main.pdf"
    }
    if (-not (Test-Path -LiteralPath $buildLog -PathType Leaf)) {
        throw "Tectonic exited successfully but did not create main.log"
    }

    $fatalPatterns = @(
        "LaTeX Error",
        "Undefined control sequence",
        "Citation.*undefined",
        "Reference.*undefined",
        "There were undefined references",
        "Overfull \\hbox",
        "Overfull \\vbox"
    )
    $logFailures = Select-String -LiteralPath $buildLog `
        -Pattern $fatalPatterns -CaseSensitive:$false
    if ($logFailures) {
        $logFailures | ForEach-Object {
            Write-Error ("main.log:{0}: {1}" -f $_.LineNumber, $_.Line)
        }
        throw "The TeX log failed the release gate"
    }

    $targetPdf = Join-Path $OutputDirectory $artifactName
    Copy-Item -LiteralPath $builtPdf -Destination $targetPdf -Force
    $hash = Get-FileHash -Algorithm SHA256 -LiteralPath $targetPdf
    $size = (Get-Item -LiteralPath $targetPdf).Length

    Write-Host "Release PDF: $targetPdf"
    Write-Host "Bytes: $size"
    Write-Host "SHA256: $($hash.Hash)"
    Write-Host "TeX log gate: PASS"
}
finally {
    if ($KeepBuildDirectory) {
        Write-Host "Build directory retained: $buildDirectory"
    }
    elseif (Test-Path -LiteralPath $buildDirectory) {
        $resolvedBuild = [System.IO.Path]::GetFullPath($buildDirectory)
        $resolvedTemp = [System.IO.Path]::GetFullPath(
            [System.IO.Path]::GetTempPath()
        )
        if (-not $resolvedBuild.StartsWith(
            $resolvedTemp,
            [System.StringComparison]::OrdinalIgnoreCase
        )) {
            throw "Refusing to remove a build directory outside the temp root"
        }
        Remove-Item -LiteralPath $resolvedBuild -Recurse -Force
    }
}
