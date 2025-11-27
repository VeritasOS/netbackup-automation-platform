@REM $Copyright: Copyright (c) 2025 Cohesity, Inc. All rights reserved $

@echo off

REM Check for correct number of arguments
if "%~4"=="" goto usage

REM Validate arguments
if "%~1"=="-wix_path" (
    set wix_path=%~2
) else (
    goto usage
)

if "%~3"=="-eeb_ver" (
    set eeb_ver=%~4
) else (
    goto usage
)

if "%~5"=="-nb_ver" (
    set nb_ver=%~6
) else (
    goto usage
)

if "%~7"=="-nb_base_installpath" (
    set nb_base_installpath=%~8
) else (
    goto usage
)

echo,
echo Performing actions with :-
echo wix_path       : %wix_path%
echo eeb_ver        : %eeb_ver%
echo nb_ver         : %nb_ver%
echo nb_base_installpath : %nb_base_installpath%

echo,
set PATH=%PATH%;%wix_path%
copy NUL %CD%\EEB-%eeb_ver%
candle %CD%\EEB_Marker.wxs -dEEB_VER=%eeb_ver% -dNB_VERSION=%nb_ver% -dBASE_INSTALL_PATH="%nb_base_installpath%" -dSOURCE_PATH=%CD% -o %CD%\obj\ -sw1075
light %CD%\obj\EEB_Marker.wixobj -o "bin\Veritas NetBackup Client EEB (%eeb_ver%).msi" -sw1076

goto :eof

:usage
echo Usage: %~n0 -wix_path=value -eeb_ver=value -nb_ver=value -nb_base_installpath=value
echo    -wix_path         : The location where wix toolset are kept.
echo    -eeb_ver          : The eeb version in SET_VERSION format. For e.g 4102406_11
echo    -nb_ver           : The NetBackup version in major.minor.patch.build format. For e.g. 10.1.1.0
echo    -nb_base_installpath   : NetBackup Client installation directory. e.g. "C:\Program Files\Veritas"
exit /b 1
