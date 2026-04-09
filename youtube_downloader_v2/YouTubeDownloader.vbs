Dim objShell, objFSO, scriptPath, progressFile
Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

scriptPath = objFSO.GetParentFolderName(WScript.ScriptFullName)
progressFile = scriptPath & "\progress.txt"

Dim htmlFile
htmlFile = scriptPath & "\gui.html"

Dim ts
Set ts = objFSO.CreateTextFile(htmlFile, True)

ts.WriteLine "<!DOCTYPE html>"
ts.WriteLine "<html><head><title>YouTube Downloader</title>"
ts.WriteLine "<style>"
ts.WriteLine "body{font-family:Segoe UI,Arial,sans-serif;margin:20px;background:#f0f0f0}"
ts.WriteLine "#box{background:white;padding:20px;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.1);max-width:480px;margin:0 auto}"
ts.WriteLine "h1{margin:0 0 20px 0;color:#c00;font-size:24px;text-align:center}"
ts.WriteLine "input{width:100%;padding:10px;font-size:14px;border:1px solid #ccc;border-radius:4px;box-sizing:border-box;margin-bottom:10px}"
ts.WriteLine "button{width:100%;padding:12px;font-size:16px;background:#c00;color:white;border:none;border-radius:4px;cursor:pointer}"
ts.WriteLine "button:hover{background:#a00}"
ts.WriteLine "button:disabled{background:#999;cursor:not-allowed}"
ts.WriteLine "#status{margin-top:15px;padding:10px;background:#f5f5f5;border-radius:4px;font-size:13px;min-height:40px}"
ts.WriteLine "#progress{width:100%;height:20px;background:#ddd;border-radius:10px;overflow:hidden;margin-top:10px;display:none}"
ts.WriteLine "#bar{height:100%;background:#c00;width:0%;transition:width 0.3s}"
ts.WriteLine "</style></head><body>"
ts.WriteLine "<div id='box'>"
ts.WriteLine "<h1>YouTube Downloader</h1>"
ts.WriteLine "<input type='text' id='url' placeholder='Paste YouTube URL here...'/>"
ts.WriteLine "<button id='btn' onclick='startDownload()'>Download</button>"
ts.WriteLine "<div id='progress'><div id='bar'></div></div>"
ts.WriteLine "<div id='status'>Ready. Paste URL and click Download.</div>"
ts.WriteLine "</div>"
ts.WriteLine "<script>"
ts.WriteLine "var fso = new ActiveXObject('Scripting.FileSystemObject');"
ts.WriteLine "var WshShell = new ActiveXObject('WScript.Shell');"
ts.WriteLine "var downloading = false;"
ts.WriteLine "var intervalId = null;"
ts.WriteLine "function startDownload(){"
ts.WriteLine "  var url = document.getElementById('url').value.trim();"
ts.WriteLine "  if(!url){alert('Please enter a URL');return;}"
ts.WriteLine "  if(url.indexOf('youtube')==-1 && url.indexOf('youtu.be')==-1){alert('Invalid YouTube URL');return;}"
ts.WriteLine "  document.getElementById('btn').disabled = true;"
ts.WriteLine "  document.getElementById('progress').style.display = 'block';"
ts.WriteLine "  document.getElementById('status').innerHTML = 'Starting...';"
ts.WriteLine "  downloading = true;"

' Build command line - use chr(34) for quotes
ts.WriteLine "  var cmd = 'python """ & Replace(scriptPath, "\", "\\") & "\\download.py"" ""' + url + '"" """ & Replace(progressFile, "\", "\\") & """';"
ts.WriteLine "  WshShell.Run(cmd, 0, false);"
ts.WriteLine "  intervalId = setInterval(checkProgress, 500);"
ts.WriteLine "}"
ts.WriteLine "function checkProgress(){"
ts.WriteLine "  if(!downloading) return;"
ts.WriteLine "  try{"
ts.WriteLine "    var ts = fso.OpenTextFile('" & Replace(progressFile, "\", "\\") & "', 1, false);"
ts.WriteLine "    var content = ts.ReadAll();"
ts.WriteLine "    ts.Close();"
ts.WriteLine "    var lines = content.split(String.fromCharCode(10));"
ts.WriteLine "    var lastLine = lines[lines.length-1] || lines[lines.length-2];"
ts.WriteLine "    if(!lastLine) return;"
ts.WriteLine "    if(lastLine.indexOf('PROGRESS:')==0){"
ts.WriteLine "      var parts = lastLine.substring(9).split('|');"
ts.WriteLine "      var pct = parts[0].trim();"
ts.WriteLine "      var speed = parts[1] || 'N/A';"
ts.WriteLine "      document.getElementById('bar').style.width = pct;"
ts.WriteLine "      document.getElementById('status').innerHTML = 'Downloading: ' + pct + '<br>Speed: ' + speed;"
ts.WriteLine "    }else if(lastLine.indexOf('DONE:')==0){"
ts.WriteLine "      document.getElementById('bar').style.width = '100%';"
ts.WriteLine "      document.getElementById('status').innerHTML = 'Complete: ' + lastLine.substring(5);"
ts.WriteLine "      document.getElementById('btn').disabled = false;"
ts.WriteLine "      downloading = false;"
ts.WriteLine "      clearInterval(intervalId);"
ts.WriteLine "    }else if(lastLine.indexOf('ERROR:')==0){"
ts.WriteLine "      document.getElementById('status').innerHTML = 'Error: ' + lastLine.substring(6);"
ts.WriteLine "      document.getElementById('btn').disabled = false;"
ts.WriteLine "      downloading = false;"
ts.WriteLine "      clearInterval(intervalId);"
ts.WriteLine "    }else{"
ts.WriteLine "      document.getElementById('status').innerHTML = lastLine;"
ts.WriteLine "    }"
ts.WriteLine "  }catch(e){}"
ts.WriteLine "}"
ts.WriteLine "</script></body></html>"

ts.Close
Set ts = Nothing

Dim ie
Set ie = CreateObject("InternetExplorer.Application")
ie.Navigate "file://" & htmlFile
ie.ToolBar = False
ie.StatusBar = False
ie.Width = 520
ie.Height = 350
ie.Left = (objShell.ScreenWidth - 520) \ 2
ie.Top = (objShell.ScreenHeight - 350) \ 2
ie.Visible = True

Do While ie.Visible
    WScript.Sleep 100
Loop

ie.Quit
Set ie = Nothing

If objFSO.FileExists(htmlFile) Then objFSO.DeleteFile htmlFile
If objFSO.FileExists(progressFile) Then objFSO.DeleteFile progressFile

Set objShell = Nothing
Set objFSO = Nothing
