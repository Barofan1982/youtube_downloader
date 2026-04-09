' YouTube 视频下载器 - VBS GUI
' 调用 Python 脚本进行下载

Option Explicit

Dim objShell, objFSO, scriptPath, pythonScript
Dim url, quality, outputDir
Dim result

' 初始化
Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' 获取当前目录
scriptPath = objFSO.GetParentFolderName(WScript.ScriptFullName)
pythonScript = scriptPath & "\youtube_downloader.py"

' 检查 Python 脚本是否存在
If Not objFSO.FileExists(pythonScript) Then
    MsgBox "错误：找不到 youtube_downloader.py" & vbCrLf & "请在同一目录下放置 Python 脚本。", vbCritical, "错误"
    WScript.Quit 1
End If

' 主循环
Do
    result = ShowMainMenu()
    If result = False Then Exit Do
Loop

Set objShell = Nothing
Set objFSO = Nothing

' ============================================
' 主菜单
' ============================================
Function ShowMainMenu()
    Dim choice
    choice = InputBox("YouTube 视频下载器" & vbCrLf & vbCrLf & _
                      "请选择操作：" & vbCrLf & vbCrLf & _
                      "1 - 下载视频 (最高画质)" & vbCrLf & _
                      "2 - 下载视频 (1080p)" & vbCrLf & _
                      "3 - 下载视频 (2K)" & vbCrLf & _
                      "4 - 下载视频 (4K)" & vbCrLf & _
                      "5 - 仅下载音频 (MP3)" & vbCrLf & _
                      "6 - 批量下载视频" & vbCrLf & _
                      "0 - 退出" & vbCrLf & vbCrLf & _
                      "请输入选项 (0-6):", "YouTube 下载器", "1")

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
            MsgBox "无效的选项，请重新输入", vbExclamation, "提示"
            ShowMainMenu = True
    End Select
End Function

' ============================================
' 下载视频
' ============================================
Sub DownloadVideo(qualityChoice)
    Dim url, quality, cmd, qualityText

    url = InputBox("请输入 YouTube 视频 URL：" & vbCrLf & vbCrLf & _
                   "支持格式：" & vbCrLf & _
                   "- https://youtube.com/watch?v=xxxxx" & vbCrLf & _
                   "- https://youtu.be/xxxxx" & vbCrLf & _
                   "- https://youtube.com/shorts/xxxxx", _
                   "输入视频链接", "")

    If url = "" Then Exit Sub

    Select Case qualityChoice
        Case "1": quality = "best": qualityText = "最高画质"
        Case "2": quality = "1080": qualityText = "1080p"
        Case "3": quality = "2k": qualityText = "2K"
        Case "4": quality = "4k": qualityText = "4K"
    End Select

    ' 确认
    If MsgBox("即将下载视频" & vbCrLf & vbCrLf & _
              "URL: " & url & vbCrLf & _
              "画质: " & qualityText & vbCrLf & vbCrLf & _
              "点击确定开始下载...", vbOKCancel + vbInformation, "确认下载") = vbCancel Then
        Exit Sub
    End If

    ' 执行下载
    cmd = "cmd /c cd /d """ & scriptPath & """ && python youtube_downloader_cli.py """ & url & """ " & quality & """"
    objShell.Run cmd, 1, True

    MsgBox "下载命令已执行！" & vbCrLf & "文件保存在: %USERPROFILE%\Downloads\YouTube", vbInformation, "完成"
End Sub

' ============================================
' 下载音频
' ============================================
Sub DownloadAudio()
    Dim url, cmd

    url = InputBox("请输入 YouTube 视频 URL（将下载为 MP3）：" & vbCrLf & vbCrLf & _
                   "支持格式：" & vbCrLf & _
                   "- https://youtube.com/watch?v=xxxxx" & vbCrLf & _
                   "- https://youtu.be/xxxxx", _
                   "输入视频链接", "")

    If url = "" Then Exit Sub

    If MsgBox("即将下载音频 (MP3)" & vbCrLf & vbCrLf & _
              "URL: " & url & vbCrLf & vbCrLf & _
              "点击确定开始下载...", vbOKCancel + vbInformation, "确认下载") = vbCancel Then
        Exit Sub
    End If

    cmd = "cmd /c cd /d """ & scriptPath & """ && python youtube_downloader_cli.py """ & url & """ audio"""
    objShell.Run cmd, 1, True

    MsgBox "音频下载命令已执行！" & vbCrLf & "文件保存在: %USERPROFILE%\Downloads\YouTube", vbInformation, "完成"
End Sub

' ============================================
' 批量下载
' ============================================
Sub BatchDownload()
    Dim urls, urlArray, i, cmd, tempFile

    urls = InputBox("请输入多个 YouTube URL，每行一个：" & vbCrLf & vbCrLf & _
                    "示例：" & vbCrLf & _
                    "https://youtube.com/watch?v=xxxxx" & vbCrLf & _
                    "https://youtube.com/watch?v=yyyyy" & vbCrLf & _
                    "https://youtu.be/zzzzz", _
                    "批量下载", "")

    If urls = "" Then Exit Sub

    ' 创建临时文件
    tempFile = scriptPath & "\batch_urls.txt"

    ' 写入文件
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

    If MsgBox("即将批量下载 " & (UBound(urlArray) + 1) & " 个视频" & vbCrLf & vbCrLf & _
              "画质: 最高画质" & vbCrLf & vbCrLf & _
              "点击确定开始下载...", vbOKCancel + vbInformation, "确认批量下载") = vbCancel Then
        objFSO.DeleteFile tempFile
        Exit Sub
    End If

    cmd = "cmd /c cd /d """ & scriptPath & """ && python youtube_downloader_cli.py --batch """ & tempFile & """"""
    objShell.Run cmd, 1, True

    ' 清理临时文件
    If objFSO.FileExists(tempFile) Then
        objFSO.DeleteFile tempFile
    End If

    MsgBox "批量下载命令已执行！" & vbCrLf & "文件保存在: %USERPROFILE%\Downloads\YouTube", vbInformation, "完成"
End Sub
