' YouTube Downloader V2 - Simple GUI
' No popup windows, progress shown inline

Option Explicit

Dim objShell, objFSO, scriptPath, progressFile
Dim mainWindow, urlInput, statusLabel, progressBar, downloadBtn
Dim isDownloading

Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

scriptPath = objFSO.GetParentFolderName(WScript.ScriptFullName)
progressFile = scriptPath & "\progress.txt"

' Create main HTML window
Dim htmlContent
htmlContent = "<!DOCTYPE html>" & vbCrLf & _
    "<html><head><title>YouTube Downloader</title>" & vbCrLf & _
    "<style>" & vbCrLf & _
    "body{font-family:Segoe UI,Arial,sans-serif;margin:20px;background:#f0f0f0}" & vbCrLf & _
    "#box{background:white;padding:20px;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.1)}" & vbCrLf & _
    "h1{margin:0 0 20px 0;color:#c00;font-size:24px}" & vbCrLf & _
    "input{width:100%;padding:10px;font-size:14px;border:1px solid #ccc;border-radius:4px;box-sizing:border-box;margin-bottom:10px}" & vbCrLf & _
    "button{width:100%;padding:12px;font-size:16px;background:#c00;color:white;border:none;border-radius:4px;cursor:pointer}" & vbCrLf & _
    "button:hover{background:#a00}" & vbCrLf & _
    "button:disabled{background:#999;cursor:not-allowed}" & vbCrLf & _
    "#status{margin-top:15px;padding:10px;background:#f5f5f5;border-radius:4px;font-size:13px;min-height:60px}" & vbCrLf & _
    "#progress{width:100%;height:20px;background:#ddd;border-radius:10px;overflow:hidden;margin-top:10px;display:none}" & vbCrLf & _
    "#bar{height:100%;background:#c00;width:0%;transition:width 0.3s}" & vbCrLf & _
    "</style></head><body>" & vbCrLf & _
    "<div id='box'>" & vbCrLf & _
    "<h1>YouTube Downloader</h1>" & vbCrLf & _
    "<input type='text' id='url' placeholder='Paste YouTube URL here...' />" & vbCrLf & _
    "<button id='btn' onclick='startDownload()'>Download</button>" & vbCrLf & _
    "<div id='progress'><div id='bar'></div></div>" & vbCrLf & _
    "<div id='status'>Ready. Paste URL and click Download.</div>" & vbCrLf & _
    "</div>" & vbCrLf & _
    "<script>" & vbCrLf & _
    "var fso = new ActiveXObject('Scripting.FileSystemObject');" & vbCrLf & _
    "var WshShell = new ActiveXObject('WScript.Shell');" & vbCrLf & _
    "var downloading = false;" & vbCrLf & _
    "function startDownload(){" & vbCrLf & _
    "  var url = document.getElementById('url').value.trim();" & vbCrLf & _
    "  if(!url){alert('Please enter a URL');return;}" & vbCrLf & _
    "  if(url.indexOf('youtube')==-1 && url.indexOf('youtu.be')==-1){alert('Invalid YouTube URL');return;}" & vbCrLf & _
    "  document.getElementById('btn').disabled = true;" & vbCrLf & _
    "  document.getElementById('progress').style.display = 'block';" & vbCrLf & _
    "  document.getElementById('status').innerHTML = 'Starting...';" & vbCrLf & _
    "  downloading = true;" & vbCrLf & _
    "  WshShell.Run('python \"" & scriptPath & "\\download.py\" \"' + url + '\" \"" & progressFile & "\"', 0, false);" & vbCrLf & _
    "  setInterval(checkProgress, 500);" & vbCrLf & _
    "}" & vbCrLf & _
    "function checkProgress(){" & vbCrLf & _
    "  if(!downloading) return;" & vbCrLf & _
    "  try{" & vbCrLf & _
    "    var file = fso.OpenTextFile('" & progressFile & "', 1, false);" & vbCrLf & _
    "    var content = file.ReadAll();" & vbCrLf & _
    "    file.Close();" & vbCrLf & _
    "    var lines = content.split('\\n');" & vbCrLf & _
    "    var lastLine = lines[lines.length-2] || lines[lines.length-1];" & vbCrLf & _
    "    if(lastLine.indexOf('PROGRESS:')==0){" & vbCrLf & _
    "      var parts = lastLine.split(':')[1].split('|');" & vbCrLf & _
    "      var pct = parts[0].trim();" & vbCrLf & _
    "      var speed = parts[1] || 'N/A';" & vbCrLf & _
    "      document.getElementById('bar').style.width = pct;" & vbCrLf & _
    "      document.getElementById('status').innerHTML = 'Downloading: ' + pct + '<br>Speed: ' + speed;" & vbCrLf & _
    "    }else if(lastLine.indexOf('DONE:')==0){" & vbCrLf & _
    "      document.getElementById('bar').style.width = '100%';" & vbCrLf & _
    "      document.getElementById('status').innerHTML = 'Complete: ' + lastLine.split(':')[1];" & vbCrLf & _
    "      document.getElementById('btn').disabled = false;" & vbCrLf & _
    "      downloading = false;" & vbCrLf & _
    "    }else if(lastLine.indexOf('ERROR:')==0){" & vbCrLf & _
    "      document.getElementById('status').innerHTML = 'Error: ' + lastLine.split(':')[1];" & vbCrLf & _
    "      document.getElementById('btn').disabled = false;" & vbCrLf & _
    "      downloading = false;" & vbCrLf & _
    "    }else{" & vbCrLf & _
    "      document.getElementById('status').innerHTML = lastLine;" & vbCrLf & _
    "    }" & vbCrLf & _
    "  }catch(e){}" & vbCrLf & _
    "}" & vbCrLf & _
    "</script></body></html>"

' Save HTML to temp file
Dim htmlFile
htmlFile = scriptPath & "\gui.html"
Dim ts
Set ts = objFSO.CreateTextFile(htmlFile, True)
ts.Write htmlContent
ts.Close
Set ts = Nothing

' Open in IE/HTA mode
Dim ie
Set ie = CreateObject("InternetExplorer.Application")
ie.Navigate "file://" & htmlFile
ie.ToolBar = False
ie.StatusBar = False
ie.Width = 500
ie.Height = 350
ie.Left = (objShell.ScreenWidth - 500) \ 2
ie.Top = (objShell.ScreenHeight - 350) \ 2
ie.Visible = True

' Wait for window to close
Do While ie.Visible
    WScript.Sleep 100
Loop

' Cleanup
ie.Quit
Set ie = Nothing
If objFSO.FileExists(htmlFile) Then objFSO.DeleteFile htmlFile
If objFSO.FileExists(progressFile) Then objFSO.DeleteFile progressFile

Set objShell = Nothing
Set objFSO = Nothing
