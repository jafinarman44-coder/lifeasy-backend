# Fix Network Connectivity for Lifeasy Backend
# Run this script as ADMINISTRATOR

Write-Host "`n=== LIFEAASY NETWORK FIX ===" -ForegroundColor Cyan
Write-Host "This script will fix the No route to host error`n" -ForegroundColor Yellow

# Step 1: Disable Firewall temporarily
Write-Host "Step 1: Disabling Firewall temporarily..." -ForegroundColor Yellow
netsh advfirewall set allprofiles state off
Write-Host "FIREWALL DISABLED" -ForegroundColor Green

# Step 2: Verify backend is running
Write-Host "`nStep 2: Checking backend server..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://192.168.0.181:8000/api/status" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "Backend is running on port 8000" -ForegroundColor Green
    }
} catch {
    Write-Host "Backend is NOT running! Run: python main.py" -ForegroundColor Red
    Write-Host "in backend folder first!" -ForegroundColor Red
}

# Step 3: Show test URL
Write-Host "`nStep 3: Test from your PHONE (192.168.0.121)" -ForegroundColor Yellow
Write-Host "Open Chrome on phone and visit:" -ForegroundColor White
Write-Host "http://192.168.0.181:8000/api/status" -ForegroundColor Cyan

Write-Host "`nIf it works, your app login will work!" -ForegroundColor Green
Write-Host "`nPress any key to re-enable firewall when done testing..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Step 4: Re-enable Firewall
Write-Host "`nRe-enabling firewall..." -ForegroundColor Yellow
netsh advfirewall set allprofiles state on
Write-Host "FIREWALL RE-ENABLED" -ForegroundColor Green

Write-Host "`nDone!" -ForegroundColor Cyan
