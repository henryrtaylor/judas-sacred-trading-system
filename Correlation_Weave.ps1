$env:PYTHONPATH = "$PSScriptRoot\.."
$python = "$PSScriptRoot\..\.venv\Scripts\python.exe"
$script = "$PSScriptRoot\..\judas-reflective-intelligence\phase16_mosaic\correlation_weave.py"
& $python $script --symbols AAPL SPY BTC-USD