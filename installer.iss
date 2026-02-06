; --- Scale Report Installer Script ---
; Created for Ahsanur Rahman

[Setup]
AppName=Scale Report
AppVersion=2.6.0
AppPublisher=Ahsanur Rahman
DefaultDirName={pf}\Scale Report
DefaultGroupName=Scale Report
UninstallDisplayIcon={app}\Scale Report.exe
OutputDir=dist
OutputBaseFilename=ScaleReportSetup
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
Source: "dist\Scale Report.exe"; DestDir: "{app}"; Flags: ignoreversion
;Source: "weights.db"; DestDir: "{app}"; Flags: ignoreversion
; Optional: include any additional files (like database, icons, or fonts)
; Example:
; Source: "dist\*"; DestDir: "{app}\data"; Flags: ignoreversion recursesubdirs

[Dirs]
Name: "{commonappdata}\ScaleReport"; Permissions: users-full

[Icons]
Name: "{group}\Scale Report"; Filename: "{app}\Scale Report.exe"
Name: "{commondesktop}\Scale Report"; Filename: "{app}\Scale Report.exe"

[Run]
Filename: "{app}\Scale Report.exe"; Description: "Launch Scale Report after installation"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Clean up any leftover files
Type: filesandordirs; Name: "{app}\data"