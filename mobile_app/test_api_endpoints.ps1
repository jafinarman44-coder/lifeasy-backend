# 🎯 LIFEASY API END-TO-END DIAGNOSTIC
# Tests all critical endpoints with colored output

$baseUrl = "https://lifeasy-api.onrender.com/api"
$passCount = 0
$failCount = 0
$totalTests = 0

function Test-Endpoint {
    param(
        [string]$Name,
        [string]$Method = "GET",
        [string]$Endpoint,
        [hashtable]$Body = $null,
        [int]$ExpectedStatus = 200
    )

    $totalTests++
    $url = "$baseUrl$Endpoint"
    
    Write-Host "`nTEST $totalTests`: $Name" -ForegroundColor Cyan
    Write-Host "   URL: $Method $url" -ForegroundColor DarkGray

    try {
        $params = @{
            Uri = $url
            Method = $Method
            UseBasicParsing = $true
            TimeoutSec = 30
        }

        if ($Body) {
            $params.Body = ($Body | ConvertTo-Json)
            $params.ContentType = "application/json"
        }

        $response = Invoke-WebRequest @params
        $statusCode = $response.StatusCode
        $content = $response.Content

        if ($statusCode -eq $ExpectedStatus) {
            Write-Host "   PASS - Status: $statusCode" -ForegroundColor Green
            Write-Host "   Response: $($content.Substring(0, [Math]::Min(150, $content.Length)))" -ForegroundColor DarkGray
            $script:passCount++
            return $true
        } else {
            Write-Host "   FAIL - Expected: $ExpectedStatus, Got: $statusCode" -ForegroundColor Red
            $script:failCount++
            return $false
        }
    } catch {
        $script:failCount++
        Write-Host "   FAIL - Error: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

Write-Host "=== LIFEASY PRODUCTION API DIAGNOSTIC TEST ===" -ForegroundColor Yellow
Write-Host "`nBase URL: $baseUrl" -ForegroundColor White

# TEST 1: Health Check (if exists)
Test-Endpoint -Name "Tenants List" -Endpoint "/tenants/all"

# TEST 2: Auth - Send OTP
Test-Endpoint -Name "Send OTP (Login Flow)" -Method "POST" -Endpoint "/otp/send" -Body @{
    tenant_id = "test@example.com"
    password = "testpass123"
} -ExpectedStatus 401  # Expected to fail with invalid creds

# TEST 3: Auth - Login V2
Test-Endpoint -Name "Login V2 (Valid Creds)" -Method "POST" -Endpoint "/auth/v2/login" -Body @{
    email = "majadar1din@gmail.com"
    password = "Jewel123!"
}

# TEST 4: Auth - Register Request
Test-Endpoint -Name "Register Request (New User)" -Method "POST" -Endpoint "/auth/v2/register-request" -Body @{
    email = "test_new_$(Get-Date -Format 'yyyyMMddHHmmss')@test.com"
    phone = "01700000000"
    name = "Test User"
}

# TEST 5: Bills Endpoint (Public)
Test-Endpoint -Name "Get Bills (Tenant: 1)" -Endpoint "/bills/tenant/1"

# TEST 6: Payments Endpoint (Public)
Test-Endpoint -Name "Get Payments (Tenant: 1)" -Endpoint "/payments/tenant/1"

# TEST 7: Check Email Autofill
Test-Endpoint -Name "Check Email Autofill" -Endpoint "/auth/v2/check-email/majadar1din@gmail.com"

# SUMMARY
Write-Host "`n=== TEST SUMMARY ===" -ForegroundColor Yellow
Write-Host "`nPASSED: $passCount" -ForegroundColor Green
Write-Host "FAILED: $failCount" -ForegroundColor Red
Write-Host "TOTAL: $totalTests" -ForegroundColor White

if ($failCount -eq 0) {
    Write-Host "`nALL TESTS PASSED! Backend is fully operational." -ForegroundColor Green
    exit 0
} else {
    Write-Host "`nSome tests failed. Check logs above for details." -ForegroundColor Yellow
    exit 1
}
