@echo off
setlocal enabledelayedexpansion

for %%F in (*pitapy*) do (
    set "filename=%%~nF"
    set "filename=!filename:pitapy=pitapy!"
    ren "%%F" "!filename!%%~xF"
)

endlocal