' YouTube Downloader V2 - Launcher
' Hide console and launch Python GUI

Option Explicit

Dim objShell, objFSO, scriptPath, pythonScript

Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

scriptPath = objFSO.GetParentFolderName(WScript.ScriptFullName)
pythonScript = scriptPath & "\gui.py"

' Check if Python script exists
If Not objFSO.FileExists(pythonScript) Then
    MsgBox "Error: Cannot find gui.py" & vbCrLf & "Please ensure gui.py is in the same folder.", vbCritical, "Error"
    WScript.Quit 1
End If

' Launch Python GUI with hidden window
' 0 = hidden window, false = don't wait
objShell.Run "python """ & pythonScript & """", 0, False

Set objShell = Nothing
Set objFSO = Nothing
