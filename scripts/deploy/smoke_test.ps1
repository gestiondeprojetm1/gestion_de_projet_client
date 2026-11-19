param(
    [Parameter(Mandatory = $true)]
    [string]$BaseUrl,
    [string]$ExpectedVersion
)

$healthUrl = "$($BaseUrl.TrimEnd('/'))/health"
$response = Invoke-RestMethod -Uri $healthUrl -Method Get -TimeoutSec 10

if ($response.status -ne 'ok' -or $response.database -ne 'ok') {
    throw "Smoke test échoué : service=$($response.status), database=$($response.database)"
}

if ($ExpectedVersion -and $response.version -ne $ExpectedVersion) {
    throw "Version inattendue : attendue=$ExpectedVersion, reçue=$($response.version)"
}

Write-Output "Smoke test OK : version=$($response.version), commit=$($response.commit)"
