; --- Scale Report Installer Script ---
; Created for Ahsanur Rahman

[Setup]
AppName=Scale ReportCLI
AppVersion=1.7.5
AppPublisher=Ahsanur Rahman
DefaultDirName={pf}\Scale ReportCLI
DefaultGroupName=Scale ReportCLI
UninstallDisplayIcon={app}\Scale ReportCLI.exe
OutputDir=dist
OutputBaseFilename=Install Scale ReportCLI
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin
SetupIconFile=favicon.ico
WizardStyle=modern
DisableDirPage=no
DisableProgramGroupPage=no
AllowCancelDuringInstall=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "dist\Scale ReportCLI.exe"; DestDir: "{app}"; Flags: ignoreversion
;Source: "weights.db"; DestDir: "{app}"; Flags: ignoreversion
; Optional: include any additional files (like database, icons, or fonts)
; Example:
; Source: "dist\*"; DestDir: "{app}\data"; Flags: ignoreversion recursesubdirs

[Dirs]
Name: "{commonappdata}\ScaleReport"; Permissions: users-full

[Icons]
Name: "{group}\Scale ReportCLI"; Filename: "{app}\Scale ReportCLI.exe"
Name: "{commondesktop}\Scale ReportCLI"; Filename: "{app}\Scale ReportCLI.exe"

[Run]
Filename: "{app}\Scale ReportCLI.exe"; Description: "Launch Scale Report after installation"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Clean up any leftover files
Type: filesandordirs; Name: "{app}\data"