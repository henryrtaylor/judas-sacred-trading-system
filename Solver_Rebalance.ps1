$today = Get-Date -Format "yyyy-MM-dd"
$year, $month, $day = $today -split "-"

# Generate the first 10 business days of this month
$start = Get-Date "$year-$month-01"
$dates = 1..15 | ForEach-Object { $start.AddDays($_ - 1) } | Where-Object {
    $_.DayOfWeek -notin 'Saturday','Sunday'
}
$secondTradingDay = ($dates | Select-Object -First 2)[-1].ToString("yyyy-MM-dd")

if ($today -eq $secondTradingDay) {
    Write-Output "Today is the 2nd trading day. Running solver rebalance..."
    $env:PYTHONPATH = "$PSScriptRoot\\.."
    $python = "$PSScriptRoot\\..\\.venv\\Scripts\\python.exe"
    $script = "$PSScriptRoot\\..\\judas-reflective-intelligence\\phase16_mosaic\\run_solver.py"
    & $python $script
} else {
    Write-Output "Not the 2nd trading day ($secondTradingDay). Exiting."
}