#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import zipfile
import logging
import tempfile
from datetime import datetime

class ZipService:
    """Serviço para compactação de arquivos"""
    
    def __init__(self):
        """Inicializa o serviço de compactação"""
        self.logger = logging.getLogger("XMLSender.ZipService")

    def compress_files(self, files, output_path=None, organize_by_type=True):
        """
        Compacta arquivos em um arquivo ZIP.
        
        Args:
            files (dict ou list): 
                - Se dict: {'nfce': [...], 'nfe': [...]} com lista de arquivos por tipo
                - Se list: Lista de dicionários com 'filename' e 'path'
            output_path (str, optional): Caminho para salvar o arquivo ZIP
            organize_by_type (bool): Se True, organiza em pastas por tipo
            
        Returns:
            str: Caminho do arquivo ZIP criado
        """
        try:
            # Se não informou caminho, cria um temporário
            if not output_path:
                temp_dir = tempfile.gettempdir()
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = os.path.join(temp_dir, f"xml_files_{timestamp}.zip")
                
            # Garante que o diretório existe
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Determinar se é estrutura organizada ou lista simples
            if isinstance(files, dict) and organize_by_type:
                return self._compress_organized_files(files, output_path)
            elif isinstance(files, list):
                return self._compress_simple_files(files, output_path)
            else:
                raise ValueError("Formato de arquivos não suportado")
                
        except Exception as e:
            self.logger.error(f"Erro ao compactar arquivos: {e}")
            raise Exception(f"Erro ao compactar arquivos: {e}")

    def _compress_organized_files(self, files_dict, output_path):
        """
        Compacta arquivos organizados por tipo em pastas separadas.
        
        Args:
            files_dict (dict): Dicionário com 'nfce' e 'nfe' contendo listas de arquivos
            output_path (str): Caminho do arquivo ZIP
            
        Returns:
            str: Caminho do arquivo ZIP criado
        """
        total_files = 0
        
        # Cria o arquivo ZIP
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            
            # Adicionar arquivos NFCe
            if 'nfce' in files_dict and files_dict['nfce']:
                nfce_files = files_dict['nfce']
                self.logger.info(f"Adicionando {len(nfce_files)} arquivos NFCe na pasta NFCe/")
                
                for file_info in nfce_files:
                    filepath = file_info['path']
                    filename = file_info['filename']
                    
                    if os.path.exists(filepath):
                        # Caminho dentro do ZIP: NFCe/nome_do_arquivo.xml
                        zip_path = f"NFCe/{filename}"
                        zipf.write(filepath, zip_path)
                        total_files += 1
                        self.logger.debug(f"Adicionado NFCe: {filename}")
                    else:
                        self.logger.warning(f"Arquivo NFCe não encontrado: {filepath}")
            
            # Adicionar arquivos NFe
            if 'nfe' in files_dict and files_dict['nfe']:
                nfe_files = files_dict['nfe']
                self.logger.info(f"Adicionando {len(nfe_files)} arquivos NFe na pasta NFe/")
                
                for file_info in nfe_files:
                    filepath = file_info['path']
                    filename = file_info['filename']
                    
                    if os.path.exists(filepath):
                        # Caminho dentro do ZIP: NFe/nome_do_arquivo.xml
                        zip_path = f"NFe/{filename}"
                        zipf.write(filepath, zip_path)
                        total_files += 1
                        self.logger.debug(f"Adicionado NFe: {filename}")
                    else:
                        self.logger.warning(f"Arquivo NFe não encontrado: {filepath}")
        
        # Log do resultado
        self.logger.info(f"Arquivo ZIP organizado criado em {output_path} com {total_files} arquivos")
        self._log_zip_structure(output_path)
        
        return output_path

    def _compress_simple_files(self, files_list, output_path):
        """
        Compacta lista simples de arquivos (comportamento original).
        
        Args:
            files_list (list): Lista de dicionários com 'filename' e 'path'
            output_path (str): Caminho do arquivo ZIP
            
        Returns:
            str: Caminho do arquivo ZIP criado
        """
        total_files = 0
        
        # Cria o arquivo ZIP
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_info in files_list:
                filename = file_info['filename']
                filepath = file_info['path']
                
                if os.path.exists(filepath):
                    zipf.write(filepath, filename)
                    total_files += 1
                    self.logger.debug(f"Adicionado: {filename}")
                else:
                    self.logger.warning(f"Arquivo não encontrado: {filepath}")
        
        self.logger.info(f"Arquivo ZIP criado em {output_path} com {total_files} arquivos")
        return output_path

    def _log_zip_structure(self, zip_path):
        """
        Registra a estrutura do arquivo ZIP no log.
        
        Args:
            zip_path (str): Caminho do arquivo ZIP
        """
        try:
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                file_list = zipf.namelist()
                
                # Organizar por pasta
                nfce_files = [f for f in file_list if f.startswith('NFCe/')]
                nfe_files = [f for f in file_list if f.startswith('NFe/')]
                root_files = [f for f in file_list if '/' not in f]
                
                self.logger.info(f"📦 Estrutura do ZIP ({len(file_list)} arquivos total):")
                
                if nfce_files:
                    self.logger.info(f"  📁 NFCe/ ({len(nfce_files)} arquivos)")
                    for file in nfce_files[:3]:  # Mostrar apenas os primeiros 3
                        self.logger.info(f"    📄 {os.path.basename(file)}")
                    if len(nfce_files) > 3:
                        self.logger.info(f"    ... e mais {len(nfce_files) - 3} arquivos")
                
                if nfe_files:
                    self.logger.info(f"  📁 NFe/ ({len(nfe_files)} arquivos)")
                    for file in nfe_files[:3]:  # Mostrar apenas os primeiros 3
                        self.logger.info(f"    📄 {os.path.basename(file)}")
                    if len(nfe_files) > 3:
                        self.logger.info(f"    ... e mais {len(nfe_files) - 3} arquivos")
                
                if root_files:
                    self.logger.info(f"  📄 Raiz ({len(root_files)} arquivos)")
                    for file in root_files[:3]:
                        self.logger.info(f"    📄 {file}")
                    if len(root_files) > 3:
                        self.logger.info(f"    ... e mais {len(root_files) - 3} arquivos")
                        
        except Exception as e:
            self.logger.error(f"Erro ao listar estrutura do ZIP: {e}")

    def get_zip_info(self, zip_path):
        """
        Obtém informações sobre um arquivo ZIP.
        
        Args:
            zip_path (str): Caminho do arquivo ZIP
            
        Returns:
            dict: Informações do ZIP
        """
        try:
            info = {
                'path': zip_path,
                'exists': os.path.exists(zip_path),
                'size': 0,
                'file_count': 0,
                'nfce_count': 0,
                'nfe_count': 0,
                'structure': []
            }
            
            if info['exists']:
                info['size'] = os.path.getsize(zip_path)
                
                with zipfile.ZipFile(zip_path, 'r') as zipf:
                    file_list = zipf.namelist()
                    info['file_count'] = len(file_list)
                    info['structure'] = file_list
                    
                    # Contar por tipo
                    info['nfce_count'] = len([f for f in file_list if f.startswith('NFCe/')])
                    info['nfe_count'] = len([f for f in file_list if f.startswith('NFe/')])
            
            return info
            
        except Exception as e:
            self.logger.error(f"Erro ao obter informações do ZIP: {e}")
            return {'error': str(e)}

# Exemplo de uso
if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Criar instância
    zip_service = ZipService()
    
    # Exemplo 1: Arquivos organizados por tipo (NOVO)
    files_organized = {
        'nfce': [
            {'filename': 'nfce_001.xml', 'path': '/caminho/para/nfce_001.xml'},
            {'filename': 'nfce_002.xml', 'path': '/caminho/para/nfce_002.xml'}
        ],
        'nfe': [
            {'filename': 'nfe_001.xml', 'path': '/caminho/para/nfe_001.xml'},
            {'filename': 'nfe_002.xml', 'path': '/caminho/para/nfe_002.xml'}
        ]
    }
    
    # Criar ZIP organizado
    zip_path = zip_service.compress_files(files_organized, "exemplo_organizado.zip")
    print(f"ZIP organizado criado: {zip_path}")
    
    # Exemplo 2: Lista simples (comportamento original)
    files_simple = [
        {'filename': 'arquivo1.xml', 'path': '/caminho/para/arquivo1.xml'},
        {'filename': 'arquivo2.xml', 'path': '/caminho/para/arquivo2.xml'}
    ]
    
    # Criar ZIP simples
    zip_path_simple = zip_service.compress_files(files_simple, "exemplo_simples.zip", organize_by_type=False)
    print(f"ZIP simples criado: {zip_path_simple}")
    
    # Obter informações do ZIP
    info = zip_service.get_zip_info(zip_path)
    print(f"Informações do ZIP: {info}")