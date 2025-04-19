$env:PYTHONPATH = "$PSScriptRoot\.."
$python = "$PSScriptRoot\..\.venv\Scripts\python.exe"
$config = "$PSScriptRoot\..\judas-reflective-intelligence\ibkr_config.yml"
$script = "$PSScriptRoot\..\judas-reflective-intelligence\phase15_cap_sym\collect_live.py"
& $python $script --config $config --symbols AAPL SPY BTC-USD