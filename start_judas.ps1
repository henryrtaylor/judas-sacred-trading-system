# Activate Virtual Environment
Write-Host "🌟 Activating Judas environment..." -ForegroundColor Cyan
cd C:\Users\Henry\Judas-IBKR_Project
.\.venv\Scripts\Activate

# Set Environment Variables
Write-Host "🌟 Setting environment variables..." -ForegroundColor Cyan
$Env:WEB3_PROVIDER="https://eth-sepolia.g.alchemy.com/v2/UNj9nOriknO6y6XsfCOnqmuhTyFkJ3gG"
$Env:SPIRIT_PRIVATE_KEY="0xYourRealPrivateKeyHere"
$Env:SPIRIT_ROUTER_ADDRESS="0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
$Env:SPIRIT_TOKEN_ADDRESS="0xYourSpiritTokenAddressHere"
$Env:USD_TOKEN_ADDRESS="0xYourUSDTokenAddressHere"
$Env:REDIS_URL="redis://localhost:6379"

# Optional: Confirm ENV variables
Write-Host "✅ Web3 Provider:" $Env:WEB3_PROVIDER
Write-Host "✅ Spirit Router:" $Env:SPIRIT_ROUTER_ADDRESS

# Start Judas Dashboard Listener
Write-Host "🚀 Starting Judas Main Pipeline..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python dashboard/main.py"

# Start Streamlit Dashboard
Write-Host "🚀 Launching Judas Dashboard Viewer..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd dashboard; streamlit run streamlit_app.py"

# Reminder
Write-Host "🙏 Judas is now standing watch. Monitor at http://localhost:8501" -ForegroundColor Yellow
