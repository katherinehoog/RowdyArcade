@echo off

echo Aracade Menu
ECHO ...............................................
ECHO PRESS 1, 2 OR 3 to select your task, or 4 to EXIT.
ECHO ...............................................
ECHO.
ECHO 1 - Play Pong
ECHO 2 - Play Space invader
ECHO 4 - EXIT
ECHO.


SET /P M=Type 1, 2, 3, or 4 then press ENTER:
IF %M%==1 GOTO Pong
IF %M%==2 GOTO Space invader


:Pong
start C:\Users\Laptop\Desktop\game\assets\pong.py
GOTO MENU
:Space invader
cd %windir%\system32\calc.exe
start calc.exe
GOTO MENU
