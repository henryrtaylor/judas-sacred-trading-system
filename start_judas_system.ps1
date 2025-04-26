# Judas System Startup Script (.ps1)
# Launches warm-up, agents, and Telegram bridge from root

cd "C:\Users\Henry\Judas-IBKR_Project"

# Activate virtual environment
. .venv\Scripts\Activate.ps1

# Start core warm-up sequence
python .\judas_reflective_intelligence\judas_warm_up.py

# Start Telegram bot bridge (run in background if desired)
Start-Process powershell -ArgumentList 'python .\judas_reflective_intelligence\phase23_telegram\telegram_bridge.py'

# (Optional) Start dashboards or agent monitoring
# Start-Process powershell -ArgumentList 'python .\judas-reflective-intelligence\judas_dash.py'

Write-Host "✅ Judas warm-up complete. Telegram interface online. Ready for command input."