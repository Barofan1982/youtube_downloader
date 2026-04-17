' AF x FB Merger - Launcher
' Hide console and launch Python GUI

Option Explicit

Dim objShell, objFSO, scriptPath, pythonScript

Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

scriptPath = objFSO.GetParentFolderName(WScript.ScriptFullName)
pythonScript = scriptPath & "\gui.py"

If Not objFSO.FileExists(pythonScript) Then
    MsgBox "Error: Cannot find gui.py" & vbCrLf & "Please ensure gui.py is in the same folder.", vbCritical, "Error"
    WScript.Quit 1
End If

' 0 = hidden window, false = don't wait
objShell.Run "python """ & pythonScript & """", 0, False

Set objShell = Nothing
Set objFSO = Nothing
