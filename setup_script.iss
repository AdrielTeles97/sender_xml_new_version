; Script para criar instalador do aplicativo "Envio de Arquivos XML"
; Versão corrigida - resolve problemas de flags
#define MyAppName "Envio de Arquivos XML"
#define MyAppVersion "2.0.0"
#define MyAppPublisher "Adriel Teles"
#define MyAppURL "http://www.suportebel.com.br/"
#define MyAppExeName "XMLSender.exe"
#define SourcePath "C:\Users\Adriel\Downloads\sender_xml_new_version\dist\"

[Setup]
AppId={{B27F1C11-8A38-4F35-9D35-9C63ED6CF9C5}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={localappdata}\{#MyAppName}
DisableProgramGroupPage=no
DefaultGroupName={#MyAppName}
OutputDir=C:\Users\Adriel\Downloads\sender_xml_new_version\output
OutputBaseFilename=EnvioArquivosXML_Setup_v{#MyAppVersion}
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=commandline
WizardStyle=modern
SetupIconFile=C:\Users\Adriel\Downloads\sender_xml_new_version\assets\icon.ico
LicenseFile=C:\Users\Adriel\Downloads\sender_xml_new_version\license.txt
AppCopyright=Copyright © {#MyAppPublisher} 2025
AppContact={#MyAppURL}
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Files]
; CORREÇÃO: Separar arquivos individuais das pastas
; Arquivo principal executável
Source: "{#SourcePath}{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; Arquivos individuais na raiz (se existirem)
Source: "{#SourcePath}*.dll"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist
Source: "{#SourcePath}*.pyd"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist
Source: "{#SourcePath}*.txt"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist



; Arquivos de configuração do projeto original (backup)
Source: "C:\Users\Adriel\Downloads\sender_xml_new_version\config\*"; DestDir: "{app}\config"; Flags: ignoreversion onlyifdoesntexist skipifsourcedoesntexist
Source: "C:\Users\Adriel\Downloads\sender_xml_new_version\assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion onlyifdoesntexist skipifsourcedoesntexist

[Dirs]
; Criar diretórios necessários com permissões corretas
Name: "{app}\config"; Permissions: users-modify
Name: "{app}\logs"; Permissions: users-modify
Name: "{app}\temp"; Permissions: users-modify
Name: "{app}\assets"

[Icons]
; Atalhos com verificação se ícone existe
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\assets\icon.ico"; Check: FileExists(ExpandConstant('{app}\assets\icon.ico'))
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; Check: not FileExists(ExpandConstant('{app}\assets\icon.ico'))

; Atalho na área de trabalho
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; Tasks: desktopicon; IconFilename: "{app}\assets\icon.ico"; Check: FileExists(ExpandConstant('{app}\assets\icon.ico'))
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; Tasks: desktopicon; Check: not FileExists(ExpandConstant('{app}\assets\icon.ico'))

; Atalho de desinstalação
Name: "{group}\Desinstalar {#MyAppName}"; Filename: "{uninstallexe}"

[Tasks]
Name: "desktopicon"; Description: "Criar ícone na área de trabalho"; GroupDescription: "Ícones adicionais:"; Flags: unchecked
Name: "quicklaunchicon"; Description: "Criar ícone na barra de tarefas"; GroupDescription: "Ícones adicionais:"; Flags: unchecked; OnlyBelowVersion: 6.1

[Registry]
; Registrar aplicativo
Root: HKCU; Subkey: "Software\{#MyAppPublisher}\{#MyAppName}"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\{#MyAppPublisher}\{#MyAppName}"; ValueType: string; ValueName: "Version"; ValueData: "{#MyAppVersion}"; Flags: uninsdeletekey

[Run]
; Executar aplicativo após instalação
Filename: "{app}\{#MyAppExeName}"; Description: "Executar {#MyAppName}"; Flags: nowait postinstall skipifsilent; WorkingDir: "{app}"

[UninstallDelete]
; Limpar arquivos criados pelo aplicativo
Type: filesandordirs; Name: "{app}\logs"
Type: filesandordirs; Name: "{app}\temp"

[Code]
// Função executada antes da instalação
function InitializeSetup(): Boolean;
var
  ExePath: String;
begin
  Result := True;
  ExePath := ExpandConstant('{#SourcePath}{#MyAppExeName}');
  
  if not FileExists(ExePath) then
  begin
    MsgBox('ERRO: O arquivo executável não foi encontrado!' + #13#10 + 
           'Caminho esperado: ' + ExePath + #13#10#13#10 + 
           'Execute primeiro o build da aplicação com PyInstaller.' + #13#10 + 
           'Comando: pyinstaller --windowed --onefile --name "main" main.py', 
           mbError, MB_OK);
    Result := False;
  end;
end;

// Função executada após a instalação
procedure CurStepChanged(CurStep: TSetupStep);
var
  ConfigFile: String;
  DefaultConfig: String;
begin
  if CurStep = ssPostInstall then
  begin
    // Criar arquivo de configuração padrão se não existir
    ConfigFile := ExpandConstant('{app}\config\settings.json');
    
    if not FileExists(ConfigFile) then
    begin
      ForceDirectories(ExpandConstant('{app}\config'));
      DefaultConfig := '{' + #13#10 +
                      '  "document_id": "",' + #13#10 +
                      '  "company_name": "",' + #13#10 +
                      '  "email": "",' + #13#10 +
                      '  "base_path": "C:\\XMLs",' + #13#10 +
                      '  "smtp": {' + #13#10 +
                      '    "server": "smtp.gmail.com",' + #13#10 +
                      '    "port": 587,' + #13#10 +
                      '    "username": "",' + #13#10 +
                      '    "password": "",' + #13#10 +
                      '    "use_tls": true' + #13#10 +
                      '  }' + #13#10 +
                      '}';
      
      SaveStringToFile(ConfigFile, DefaultConfig, False);
    end;
  end;
end;