Set UAC = CreateObject("Shell.Application")
Set fso = CreateObject("Scripting.FileSystemObject")
currentDir = fso.GetParentFolderName(WScript.ScriptFullName)

' Point to the SILENT batch file
cmdLine = "/c cd /d """ & currentDir & """ && start_silent.bat"

UAC.ShellExecute "cmd.exe", cmdLine, "", "runas", 0
