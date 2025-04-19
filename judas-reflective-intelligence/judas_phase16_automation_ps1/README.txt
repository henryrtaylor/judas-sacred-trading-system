JUDAS SCHEDULING – PHASE 16 (PowerShell Scripts)

STEP 1: Edit these .ps1 scripts if you change paths or symbols.

STEP 2: Test manually:
  Right-click > Run with PowerShell

STEP 3: Schedule with Windows Task Scheduler:
  - Open Task Scheduler
  - Create Basic Task
  - Trigger: Daily / Weekly
  - Action: Start a program
      Program: powershell.exe
      Arguments: -ExecutionPolicy Bypass -File "C:\path\to\Correlation_Weave.ps1"

STEP 4: Set 'Run whether user is logged in or not' (optional, for background mode)

-- TASKS INCLUDED --
✓ Collect_Live.ps1
✓ Correlation_Weave.ps1
✓ Solver_Rebalance.ps1 (scaffold only – implement logic inside run_solver.py)