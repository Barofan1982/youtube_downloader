' YouTube Video Downloader - VBS GUI
' Call Python script for downloading

Option Explicit

Dim objShell, objFSO, scriptPath, pythonScript
Dim url, quality, outputDir
Dim result

' Initialize
Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Get current directory
scriptPath = objFSO.GetParentFolderName(WScript.ScriptFullName)
pythonScript = scriptPath & "\youtube_downloader.py"

' Check if Python script exists
If Not objFSO.FileExists(pythonScript) Then
    MsgBox "Error: Cannot find youtube_downloader.py" & vbCrLf & "Please place Python script in the same directory.", vbCritical, "Error"
    WScript.Quit 1
End If

' Main loop
Do
    result = ShowMainMenu()
    If result = False Then Exit Do
Loop

Set objShell = Nothing
Set objFSO = Nothing

' ============================================
' Main Menu
' ============================================
Function ShowMainMenu()
    Dim choice
    choice = InputBox("YouTube Video Downloader" & vbCrLf & vbCrLf & _
                      "Please select operation:" & vbCrLf & vbCrLf & _
                      "1 - Download Video (Best Quality)" & vbCrLf & _
                      "2 - Download Video (1080p)" & vbCrLf & _
                      "3 - Download Video (2K)" & vbCrLf & _
                      "4 - Download Video (4K)" & vbCrLf & _
                      "5 - Audio Only (MP3)" & vbCrLf & _
                      "6 - Batch Download" & vbCrLf & _
                      "0 - Exit" & vbCrLf & vbCrLf & _
                      "Enter option (0-6):", "YouTube Downloader", "1")

    If choice = "" Then
        ShowMainMenu = False
        Exit Function
    End If

    Select Case Trim(choice)
        Case "0"
            ShowMainMenu = False
        Case "1", "2", "3", "4"
            Call DownloadVideo(choice)
            ShowMainMenu = True
        Case "5"
            Call DownloadAudio()
            ShowMainMenu = True
        Case "6"
            Call BatchDownload()
            ShowMainMenu = True
        Case Else
            MsgBox "Invalid option, please try again", vbExclamation, "Hint"
            ShowMainMenu = True
    End Select
End Function

' ============================================
' Download Video
' ============================================
Sub DownloadVideo(qualityChoice)
    Dim url, quality, cmd, qualityText

    url = InputBox("Please enter YouTube video URL:" & vbCrLf & vbCrLf & _
                   "Supported formats:" & vbCrLf & _
                   "- https://youtube.com/watch?v=xxxxx" & vbCrLf & _
                   "- https://youtu.be/xxxxx" & vbCrLf & _
                   "- https://youtube.com/shorts/xxxxx", _
                   "Enter Video URL", "")

    If url = "" Then Exit Sub

    Select Case qualityChoice
        Case "1": quality = "best": qualityText = "Best Quality"
        Case "2": quality = "1080": qualityText = "1080p"
        Case "3": quality = "2k": qualityText = "2K"
        Case "4": quality = "4k": qualityText = "4K"
    End Select

    ' Confirm
    If MsgBox("Ready to download video" & vbCrLf & vbCrLf & _
              "URL: " & url & vbCrLf & _
              "Quality: " & qualityText & vbCrLf & vbCrLf & _
              "Click OK to start downloading...", vbOKCancel + vbInformation, "Confirm Download") = vbCancel Then
        Exit Sub
    End If

    ' Execute download
    cmd = "cmd /c cd /d """ & scriptPath & """ && python youtube_downloader_cli.py """ & url & """ " & quality & """"
    objShell.Run cmd, 1, True

    MsgBox "Download command executed!" & vbCrLf & "Files saved to: %USERPROFILE%\Downloads\YouTube", vbInformation, "Done"
End Sub

' ============================================
' Download Audio
' ============================================
Sub DownloadAudio()
    Dim url, cmd

    url = InputBox("Please enter YouTube video URL (will download as MP3):" & vbCrLf & vbCrLf & _
                   "Supported formats:" & vbCrLf & _
                   "- https://youtube.com/watch?v=xxxxx" & vbCrLf & _
                   "- https://youtu.be/xxxxx", _
                   "Enter Video URL", "")

    If url = "" Then Exit Sub

    If MsgBox("Ready to download audio (MP3)" & vbCrLf & vbCrLf & _
              "URL: " & url & vbCrLf & vbCrLf & _
              "Click OK to start downloading...", vbOKCancel + vbInformation, "Confirm Download") = vbCancel Then
        Exit Sub
    End If

    cmd = "cmd /c cd /d """ & scriptPath & """ && python youtube_downloader_cli.py """ & url & """ audio"""
    objShell.Run cmd, 1, True

    MsgBox "Audio download command executed!" & vbCrLf & "Files saved to: %USERPROFILE%\Downloads\YouTube", vbInformation, "Done"
End Sub

' ============================================
' Batch Download
' ============================================
Sub BatchDownload()
    Dim urls, urlArray, i, cmd, tempFile

    urls = InputBox("Please enter multiple YouTube URLs, one per line:" & vbCrLf & vbCrLf & _
                    "Example:" & vbCrLf & _
                    "https://youtube.com/watch?v=xxxxx" & vbCrLf & _
                    "https://youtube.com/watch?v=yyyyy" & vbCrLf & _
                    "https://youtu.be/zzzzz", _
                    "Batch Download", "")

    If urls = "" Then Exit Sub

    ' Create temp file
    tempFile = scriptPath & "\batch_urls.txt"

    ' Write to file
    Dim ts
    Set ts = objFSO.CreateTextFile(tempFile, True)
    urlArray = Split(urls, vbCrLf)
    For i = 0 To UBound(urlArray)
        If Trim(urlArray(i)) <> "" Then
            ts.WriteLine Trim(urlArray(i))
        End If
    Next
    ts.Close
    Set ts = Nothing

    If MsgBox("Ready to batch download " & (UBound(urlArray) + 1) & " videos" & vbCrLf & vbCrLf & _
              "Quality: Best Quality" & vbCrLf & vbCrLf & _
              "Click OK to start downloading...", vbOKCancel + vbInformation, "Confirm Batch Download") = vbCancel Then
        objFSO.DeleteFile tempFile
        Exit Sub
    End If

    cmd = "cmd /c cd /d """ & scriptPath & """ && python youtube_downloader_cli.py --batch """ & tempFile & """"""
    objShell.Run cmd, 1, True

    ' Clean up temp file
    If objFSO.FileExists(tempFile) Then
        objFSO.DeleteFile tempFile
    End If

    MsgBox "Batch download command executed!" & vbCrLf & "Files saved to: %USERPROFILE%\Downloads\YouTube", vbInformation, "Done"
End Sub
