@echo off
REM ============================================================
REM  Late to KOSEN - grab Unity editor log
REM
REM  Double-click this file. It copies Unity's editor log into
REM  this project folder so the crash can actually be read.
REM
REM  Run it AFTER the crash. Unity renames Editor.log to
REM  Editor-prev.log the next time it starts, so both are copied.
REM ============================================================

set DEST=%~dp0
set SRC=%LOCALAPPDATA%\Unity\Editor

echo Copying from %SRC%
echo         to   %DEST%
echo.

if exist "%SRC%\Editor.log" (
    copy /Y "%SRC%\Editor.log" "%DEST%editor_log.txt" >nul
    echo   [ok] editor_log.txt
) else (
    echo   [--] Editor.log not found
)

if exist "%SRC%\Editor-prev.log" (
    copy /Y "%SRC%\Editor-prev.log" "%DEST%editor_log_prev.txt" >nul
    echo   [ok] editor_log_prev.txt
) else (
    echo   [--] Editor-prev.log not found
)

echo.
echo Done. Tell Claude the files are ready.
pause
