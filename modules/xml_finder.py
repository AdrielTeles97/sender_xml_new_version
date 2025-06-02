#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import logging
import xml.etree.ElementTree as ET
from datetime import datetime

class XMLFinder:
    """Classe para encontrar arquivos XML baseados em critérios específicos"""
    
    def __init__(self, base_path):
        """
        Inicializa o buscador de arquivos XML.
        
        Args:
            base_path (str): Caminho base para a busca de arquivos
        """
        self.base_path = base_path
        self.logger = logging.getLogger("XMLSender.XMLFinder")
    
    def find_xml_files(self, document_id, period):
        """
        Encontra arquivos XML com base no CPF/CNPJ e período.
        
        Args:
            document_id (str): CPF/CNPJ (apenas números)
            period (str): Período no formato YYYYMM
            
        Returns:
            dict: Dicionário com listas de arquivos NFCe e NFe
        """
        self.logger.info(f"Buscando arquivos para doc {document_id} no período {period}")
        
        result = {
            'nfce': [],
            'nfe': []
        }
        
        # Verificar se o diretório base existe
        if not self.base_path or not os.path.isdir(self.base_path):
            self.logger.error(f"Diretório base não encontrado: {self.base_path}")
            return result
        
        # Construir padrão de caminho para o período
        year = period[:4]
        month = period[4:6]
        
        # Buscar em diretório específico para NFC-e
        nfce_path = os.path.join(self.base_path, "NFCe", year, month)
        if os.path.isdir(nfce_path):
            self.logger.info(f"Buscando NFC-e em: {nfce_path}")
            result['nfce'] = self._find_files_by_document(nfce_path, document_id)
            self.logger.info(f"Encontrados {len(result['nfce'])} arquivos NFC-e")
        else:
            self.logger.warning(f"Diretório não encontrado: {nfce_path}")
        
        # Buscar em diretório específico para NF-e
        nfe_path = os.path.join(self.base_path, "NFe", year, month)
        if os.path.isdir(nfe_path):
            self.logger.info(f"Buscando NF-e em: {nfe_path}")
            result['nfe'] = self._find_files_by_document(nfe_path, document_id)
            self.logger.info(f"Encontrados {len(result['nfe'])} arquivos NF-e")
        else:
            self.logger.warning(f"Diretório não encontrado: {nfe_path}")
        
        return result
    
    def _find_files_by_document(self, directory, document_id):
        """
        Encontra arquivos XML que contêm o CPF/CNPJ especificado.
        
        Args:
            directory (str): Diretório para busca
            document_id (str): CPF/CNPJ (apenas números)
            
        Returns:
            list: Lista de caminhos de arquivos encontrados
        """
        found_files = []
        
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith('.xml'):
                    file_path = os.path.join(root, file)
                    try:
                        # Abrir o arquivo e verificar se contém o CPF/CNPJ
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            if document_id in content:
                                found_files.append(file_path)
                    except Exception as e:
                        self.logger.warning(f"Erro ao ler arquivo {file_path}: {e}")
        
        return found_files
    
    def find_by_period(self, period, recursive=True):
        """
        Encontra arquivos XML de um período específico.
        
        Args:
            period (str): Período no formato YYYY-MM
            recursive (bool): Se deve buscar em subdiretórios
            
        Returns:
            list: Lista de caminhos de arquivos XML
        """
        # Validar formato do período
        if not re.match(r"^\d{4}-\d{2}$", period):
            raise ValueError(f"Formato de período inválido: {period}. Use YYYY-MM")
        
        # Extrair ano e mês do período
        year, month = period.split('-')
        period_formatted = f"{year}{month}"
        
        # Buscar por arquivos que correspondam ao período
        files = self.find_all_files(recursive)
        matches = []
        
        for file in files:
            try:
                # Verificar se o arquivo corresponde ao período
                file_date = self._extract_date_from_xml(file)
                if file_date and file_date.strftime("%Y%m") == period_formatted:
                    matches.append(file)
            except Exception as e:
                self.logger.warning(f"Erro ao processar arquivo {file}: {e}")
        
        return matches
    
    def find_all_files(self, recursive=True):
        """
        Encontra todos os arquivos XML no diretório base.
        
        Args:
            recursive (bool): Se deve buscar em subdiretórios
            
        Returns:
            list: Lista de caminhos de arquivos XML
        """
        files = []
        
        if recursive:
            for root, _, filenames in os.walk(self.base_path):
                for filename in filenames:
                    if filename.lower().endswith('.xml'):
                        files.append(os.path.join(root, filename))
        else:
            for filename in os.listdir(self.base_path):
                if filename.lower().endswith('.xml'):
                    files.append(os.path.join(self.base_path, filename))
        
        return files
    
    def _extract_date_from_xml(self, file_path):
        """
        Extrai a data de emissão de um arquivo XML de NF-e ou NFC-e.
        
        Args:
            file_path (str): Caminho do arquivo XML
            
        Returns:
            datetime: Data de emissão do documento ou None se não encontrado
        """
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Namespace da NF-e
            ns = {'ns': 'http://www.portalfiscal.inf.br/nfe'}
            
            # Tentar encontrar a data de emissão
            # Primeiro, tenta no formato da NF-e
            date_elem = root.find('.//ns:dhEmi', ns)
            
            if date_elem is None:
                date_elem = root.find('.//ns:dEmi', ns)
            
            if date_elem is not None:
                date_str = date_elem.text
                
                # Formatos possíveis
                if 'T' in date_str:  # Formato com timezone: 2023-01-01T14:30:00-03:00
                    return datetime.fromisoformat(date_str)
                else:  # Formato simples: 2023-01-01
                    return datetime.strptime(date_str, '%Y-%m-%d')
        
        except Exception as e:
            self.logger.warning(f"Erro ao extrair data do arquivo {file_path}: {e}")
            
        return None