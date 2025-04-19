$env:PYTHONPATH = "$PSScriptRoot\.."
$python = "$PSScriptRoot\..\.venv\Scripts\python.exe"
$script = "$PSScriptRoot\..\judas-reflective-intelligence\phase16_mosaic\run_solver.py"
& $python $script