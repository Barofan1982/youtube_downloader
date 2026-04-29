' YouTube Downloader V2 - Launcher
' Launch the tkinter GUI without a console window

Option Explicit

Dim objShell, objFSO, scriptPath, pythonScript, pythonExe, logFile, command

Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

scriptPath = objFSO.GetParentFolderName(WScript.ScriptFullName)
pythonScript = scriptPath & "\gui.py"
logFile = scriptPath & "\launcher_error.log"

' Check if Python script exists
If Not objFSO.FileExists(pythonScript) Then
    MsgBox "Error: Cannot find gui.py" & vbCrLf & "Please ensure gui.py is in the same folder.", vbCritical, "Error"
    WScript.Quit 1
End If

' Prefer pythonw.exe so the console stays hidden while the GUI remains visible.
pythonExe = ""
On Error Resume Next
pythonExe = objShell.Exec("where pythonw").StdOut.ReadLine()
If Err.Number <> 0 Or pythonExe = "" Then
    Err.Clear
    pythonExe = objShell.Exec("where python").StdOut.ReadLine()
End If
On Error GoTo 0

If pythonExe = "" Then
    MsgBox "Error: Python was not found in PATH." & vbCrLf & "Please install Python or add it to PATH.", vbCritical, "Error"
    WScript.Quit 1
End If

command = """" & pythonExe & """ """ & pythonScript & """"

' 1 = normal window. With pythonw.exe this shows the tkinter GUI without a console.
objShell.Run command, 1, False

Set objShell = Nothing
Set objFSO = Nothing
