; Script para criar instalador do aplicativo "Envio de Arquivos XML"

#define MyAppName "Envio de Arquivos XML"
#define MyAppVersion "2.0.0"
#define MyAppPublisher "Adriel Teles"
#define MyAppURL "http://www.suportebel.com.br/"
#define MyAppExeName "main.exe"
#define SourcePath "C:\Users\Adriel\Downloads\sender_xml_new_version\dist\main"

[Setup]
AppId={{B27F1C11-8A38-4F35-9D35-9C63ED6CF9C5}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=C:\Users\Adriel\Downloads\sender_xml_new_version\output
OutputBaseFilename=EnvioArquivosXML_Setup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Adiciona todos os arquivos da pasta dist\main
Source: "{#SourcePath}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Flags: runasadmin
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; Flags: runasadmin

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent runasadmin