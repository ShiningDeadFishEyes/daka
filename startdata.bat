@echo off 　　
if "%1" == "h" goto begin 
    mshta vbscript:createobject("wscript.shell").run("%~nx0 h",0)(window.close)&&exit 
:begin 
python "D:\my program\daka\main.py" >>  "D:\my program\daka\log.txt" 
pause;