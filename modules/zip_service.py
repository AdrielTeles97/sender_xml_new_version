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
    
    def compress_files(self, files, output_path=None):
        """
        Compacta arquivos em um arquivo ZIP.
        
        Args:
            files (list): Lista de dicionários com 'filename' e 'path'
            output_path (str, optional): Caminho para salvar o arquivo ZIP
            
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
            
            # Cria o arquivo ZIP
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_info in files:
                    filename = file_info['filename']
                    filepath = file_info['path']
                    
                    if os.path.exists(filepath):
                        zipf.write(filepath, filename)
                    else:
                        self.logger.warning(f"Arquivo não encontrado: {filepath}")
            
            self.logger.info(f"Arquivo ZIP criado em {output_path} com {len(files)} arquivos")
            return output_path
        
        except Exception as e:
            self.logger.error(f"Erro ao compactar arquivos: {e}")
            raise Exception(f"Erro ao compactar arquivos: {e}")