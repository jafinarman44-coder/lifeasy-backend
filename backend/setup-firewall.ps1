# Firewall Configuration for FastAPI Backend
# Run this script as Administrator

Write-Host "=== Adding Firewall Rules for FastAPI Port 8000 ===" -ForegroundColor Cyan

# Add inbound rule
Write-Host "`n[1/2] Adding INBOUND firewall rule..." -ForegroundColor Yellow
netsh advfirewall firewall add rule name="FastAPI8000-IN" dir=in action=allow protocol=TCP localport=8000

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Inbound rule added successfully!" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to add inbound rule. Error code: $LASTEXITCODE" -ForegroundColor Red
}

# Add outbound rule
Write-Host "`n[2/2] Adding OUTBOUND firewall rule..." -ForegroundColor Yellow
netsh advfirewall firewall add rule name="FastAPI8000-OUT" dir=out action=allow protocol=TCP localport=8000

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Outbound rule added successfully!" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to add outbound rule. Error code: $LASTEXITCODE" -ForegroundColor Red
}

Write-Host "`n=== Firewall Configuration Complete ===" -ForegroundColor Cyan
Write-Host "`nNext steps:" -ForegroundColor White
Write-Host "1. Restart your FastAPI backend server" -ForegroundColor White
Write-Host "2. Verify mobile app can connect to http://192.168.0.119:8000" -ForegroundColor White
Write-Host "`nPress any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
