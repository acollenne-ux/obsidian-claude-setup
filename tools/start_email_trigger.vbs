Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\Alexandre collenne\.claude\tools"
WshShell.Run "pythonw ""C:\Users\Alexandre collenne\.claude\tools\email_trigger.py""", 0, False
