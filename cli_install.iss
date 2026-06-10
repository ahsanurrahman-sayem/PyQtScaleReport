; debtor.iss — Inno Setup script for DebtorManager
; Tested with Inno Setup 6.x
;
; Run from Inno Setup Compiler GUI or:
;   ISCC.exe debtor.iss

#define AppName      "Scale Report CLI"
#define AppVersion   "2.6.3"
#define AppPublisher "Ahsanur Rahman"
#define AppExeName   "Scale ReportCLI.exe"
#define AppId        "{{A3F2C1D4-89B0-4E7A-9C3F-1D2E5B6A7F8D}"
#define SourceDir    "dist\ScaleReportCLI"


[Setup]
AppId={#AppId}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL=https://ahsanurrahman-sayem.github.io/ars
AppSupportURL=https://github.com/ahsanurrahman-sayem/PyQtScaleReport
AppUpdatesURL=https://github.com/ahsanurrahman-sayem/PyQtScaleReport

; Install to Program Files by default
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}


; Allow user to choose install dir
DisableDirPage=no
DisableProgramGroupPage=yes

; Compression
Compression=lzma2/ultra64
SolidCompression=yes
InternalCompressLevel=ultra64

; Output
OutputDir=installer
OutputBaseFilename={#AppNAme}_Setup_v{#AppVersion}


; Require admin so it can write to Program Files
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

; Windows version gate: Vista SP1+ (0x06000100)
;MinVersion=6.0.6001

; GUI appearance
WizardStyle=modern
SetupIconFile=assets\imgs\favicon.ico
UninstallDisplayIcon={app}\{#AppExeName}
ShowLanguageDialog=no

; Prevent running multiple instances of the installer
AppMutex=DebtorManagerSetupMutex

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon";    Description: "Create a &desktop shortcut";    GroupDescription: "Shortcuts:"; Flags: checkedonce
Name: "startmenuicon";  Description: "Create a &Start Menu shortcut"; GroupDescription: "Shortcuts:"; Flags: checkedonce

[Files]
; The entire PyInstaller onedir output
Source: "{#SourceDir}"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs


[Icons]
; Start Menu
Name: "{group}\{#AppName}";          Filename: "{app}\{#AppExeName}"; Tasks: startmenuicon
Name: "{group}\Uninstall {#AppName}"; Filename: "{uninstallexe}";      Tasks: startmenuicon

; Desktop
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Run]
; Offer to launch app right after install
Filename: "{app}\{#AppExeName}"; \
  Description: "Launch {#AppName} now"; \
  Flags: nowait postinstall skipifsilent

[UninstallRun]
; Nothing special — DB lives in %APPDATA%\DebtorManager (preserved on uninstall)

[UninstallDelete]
; Only remove app files, NOT the user's database in %APPDATA%
Type: filesandordirs; Name: "{app}"

[Code]
// ── Pre-install: kill running instance ──────────────────────────────────────
function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
begin
  // Attempt to close a running DebtorManager gracefully
  Exec('taskkill.exe', '/F /IM Scale ReportCLI.exe', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  Result := True;
end;

// ── Post-uninstall notice about user data ───────────────────────────────────
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usPostUninstall then
  begin
    MsgBox(
      'Debtor Manager has been uninstalled.' + #13#10 + #13#10 +
      'Your database file is preserved at:' + #13#10 +
      '%APPDATA%\DebtorManager\debtor.db' + #13#10 + #13#10 +
      'You can delete it manually if you no longer need it.',
      mbInformation,
      MB_OK
    );
  end;
end;