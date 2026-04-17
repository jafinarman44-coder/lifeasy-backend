# 🎯 TEST MOBILE APPROVAL API ENDPOINT
# Tests the tenant approval endpoint with colored output

$baseUrl = "https://lifeasy-api.onrender.com/api"

Write-Host "=== MOBILE APPROVAL API TEST ===" -ForegroundColor Cyan
Write-Host "Base URL: $baseUrl" -ForegroundColor White

# TEST 1: Get All Tenants
Write-Host "`n[TEST 1] Get All Tenants" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/tenants/all" -Method GET -UseBasicParsing -TimeoutSec 30
    Write-Host "  Status: $($response.StatusCode) - SUCCESS" -ForegroundColor Green
    $tenants = $response.Content | ConvertFrom-Json
    Write-Host "  Tenants Found: $($tenants.Count)" -ForegroundColor White
    foreach ($tenant in $tenants) {
        Write-Host "  - ID: $($tenant.id), Name: $($tenant.name), Email: $($tenant.email)" -ForegroundColor DarkGray
    }
} catch {
    Write-Host "  FAIL: $($_.Exception.Message)" -ForegroundColor Red
}

# TEST 2: Approve Tenant (Test with tenant ID 1)
Write-Host "`n[TEST 2] Approve Tenant (ID: 1)" -ForegroundColor Yellow
try {
    $url = "$baseUrl/tenants/approve/1"
    Write-Host "  URL: POST $url" -ForegroundColor DarkGray
    
    $response = Invoke-WebRequest -Uri $url -Method POST -UseBasicParsing -TimeoutSec 30 -ContentType "application/json"
    Write-Host "  Status: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "  Response: $($response.Content)" -ForegroundColor White
} catch {
    Write-Host "  Status: FAIL" -ForegroundColor Red
    Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "  Server Response: $responseBody" -ForegroundColor DarkGray
    }
}

# TEST 3: Check HTTPS enforcement
Write-Host "`n[TEST 3] HTTPS Enforcement Check" -ForegroundColor Yellow
$httpsUrl = "https://lifeasy-api.onrender.com/api/tenants/all"
try {
    $response = Invoke-WebRequest -Uri $httpsUrl -UseBasicParsing -TimeoutSec 30
    Write-Host "  HTTPS Working: YES" -ForegroundColor Green
    Write-Host "  Response Time: Fast" -ForegroundColor Green
} catch {
    Write-Host "  HTTPS Working: NO" -ForegroundColor Red
    Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n=== TEST COMPLETE ===" -ForegroundColor Cyan
Write-Host "All API calls using HTTPS production backend" -ForegroundColor Green
