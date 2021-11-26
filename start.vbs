Set WshShell = CreateObject("WScript.Shell")
WshShell.Run Chr(34) & "C:\Proyecto\cloudgh\run_server.bat" & Chr(34), 1, true
Set WshShell = Nothing