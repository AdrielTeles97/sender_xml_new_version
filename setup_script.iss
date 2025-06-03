; Script para criar instalador do aplicativo "Envio de Arquivos XML"
#define MyAppName "Envio de Arquivos XML"
#define MyAppVersion "2.0.0"
#define MyAppPublisher "Adriel Teles"
#define MyAppURL "http://www.suportebel.com.br/"
#define MyAppExeName "main.exe"
#define SourcePath "C:\Users\Adriel\Downloads\sender_xml_new_version\dist\"

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
PrivilegesRequiredOverridesAllowed=dialog
WizardStyle=modern
; Apontar para o arquivo de licença na pasta raiz
LicenseFile=C:\Users\Adriel\Downloads\sender_xml_new_version\license.txt

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Files]
; Adiciona todos os arquivos da pasta dist\main
Source: "{#SourcePath}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Ícone no Menu Iniciar
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
; Ícone na Área de Trabalho
Name: "{autodesktop}\Envio de Arquivos XML"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Tasks]
; Permite ao usuário escolher se quer o ícone na área de trabalho
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Registry]
; Adiciona entradas de registro para garantir que o aplicativo sempre execute como administrador
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers"; ValueType: string; ValueName: "{app}\{#MyAppExeName}"; ValueData: "RUNASADMIN"; Flags: uninsdeletekeyifempty