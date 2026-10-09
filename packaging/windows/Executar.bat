@echo off
setlocal
title MangaFire Downloader
cd /d "%~dp0"
goto start

:start
if not exist "%~dp0mangafire-dl.exe" goto missing_exe

cls
echo ========================================
echo       MangaFire Downloader @VERSION@
echo ========================================
echo.
echo This launcher makes the command-line
echo application easier to use.
echo.

set "MANGA_URL="
set /p "MANGA_URL=Paste the MangaFire URL: "
if not defined MANGA_URL goto missing_url

echo.
echo Select the URL type:
echo.
echo 1 - Direct volume or chapter URL
echo 2 - Manga page (choose volumes/chapters)
echo.

set "URL_MODE="
set /p "URL_MODE=Choose 1 or 2: "

if "%URL_MODE%"=="1" goto direct
if "%URL_MODE%"=="2" goto manga
goto invalid_mode

:direct
echo.
set "OUTPUT_DIR="
set /p "OUTPUT_DIR=Output folder (Enter for Downloads): "

if defined OUTPUT_DIR goto direct_with_output

"%~dp0mangafire-dl.exe" "%MANGA_URL%"
set "RESULT=%ERRORLEVEL%"
goto finish

:direct_with_output
"%~dp0mangafire-dl.exe" "%MANGA_URL%" --output "%OUTPUT_DIR%"
set "RESULT=%ERRORLEVEL%"
goto finish

:manga
echo.
set "LANGUAGE="
set /p "LANGUAGE=Language (e.g. pt-br or en): "
if not defined LANGUAGE goto missing_language

echo.
echo Select what to download:
echo.
echo 1 - Volumes
echo 2 - Chapters
echo.

set "RESOURCE_MODE="
set /p "RESOURCE_MODE=Choose 1 or 2: "

if "%RESOURCE_MODE%"=="1" goto volumes
if "%RESOURCE_MODE%"=="2" goto chapters
goto invalid_resource_mode

:volumes
set "RESOURCE_FLAG=--volumes"
goto get_selection

:chapters
set "RESOURCE_FLAG=--chapters"
goto get_selection

:get_selection
echo.
echo Examples: 1-5   or   1-5, 8, 12-15
set "SELECTION="
set /p "SELECTION=Numbers to download: "
if not defined SELECTION goto missing_selection

echo.
set "OUTPUT_DIR="
set /p "OUTPUT_DIR=Output folder (Enter for Downloads): "

if defined OUTPUT_DIR goto manga_with_output

"%~dp0mangafire-dl.exe" "%MANGA_URL%" --lang "%LANGUAGE%" %RESOURCE_FLAG% "%SELECTION%"
set "RESULT=%ERRORLEVEL%"
goto finish

:manga_with_output
"%~dp0mangafire-dl.exe" "%MANGA_URL%" --lang "%LANGUAGE%" %RESOURCE_FLAG% "%SELECTION%" --output "%OUTPUT_DIR%"
set "RESULT=%ERRORLEVEL%"
goto finish

:missing_exe
echo ERROR: mangafire-dl.exe was not found.
echo Keep this BAT file beside the executable.
set "RESULT=1"
goto finish

:missing_url
echo ERROR: No URL was provided.
set "RESULT=1"
goto finish

:missing_language
echo ERROR: No language was provided.
set "RESULT=1"
goto finish

:missing_selection
echo ERROR: No volumes or chapters were selected.
set "RESULT=1"
goto finish

:invalid_mode
echo ERROR: Invalid URL type. Choose 1 or 2.
set "RESULT=1"
goto finish

:invalid_resource_mode
echo ERROR: Invalid selection. Choose 1 or 2.
set "RESULT=1"
goto finish

:finish
echo.
if "%RESULT%"=="0" (
    echo Operation completed successfully.
) else (
    echo The program finished with exit code %RESULT%.
)
echo.
echo This window will remain open until you press a key.
pause >nul
exit /b %RESULT%