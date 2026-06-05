# Start Streamlit App
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; streamlit run app.py"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AI DSA Coach - Started!" -ForegroundColor Green
Write-Host "  Streamlit: http://localhost:8501" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
